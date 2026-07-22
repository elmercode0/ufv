# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('elt579/aula2/dataset_problema2.csv')

X = df.drop(['id', 'Severidade'], axis=1)
y = df['Severidade']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)
X_train_sc = pd.DataFrame(X_train_sc, columns=X_train.columns)
X_test_sc = pd.DataFrame(X_test_sc, columns=X_train.columns)

from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

max_f = 20
lista_score = list()
for i in range(1, max_f + 1):
    modelo_linear = LinearRegression()
    selector = RFE(modelo_linear, n_features_to_select=i, step=1)
    selector = selector.fit(X_train_sc, y_train)
    mask = selector.support_
    features = X_train_sc.columns
    sel_features = features[mask]
    X_sel = X_train_sc[sel_features]
    score = cross_val_score(modelo_linear, X_sel, y_train, cv=10, scoring='r2')
    lista_score.append(np.mean(score))
    print(i, np.mean(score))

best_n = int(np.argmax(lista_score)) + 1
print('Melhor n de features (baseline):', best_n, 'R2 CV =', max(lista_score))

plt.figure(figsize=(7, 4.5))
plt.plot(range(1, max_f + 1), lista_score, marker='o')
plt.axvline(best_n, color='red', linestyle='--', alpha=0.6, label=f'melhor n={best_n}')
plt.xlabel('Numero de features selecionadas (RFE)')
plt.ylabel('R2 medio (CV=10)')
plt.title('Baseline - Script Original: RFE + Regressao Linear')
plt.legend()
plt.tight_layout()
plt.savefig('elt579/aula2/relatorio_outputs/01_baseline_rfe_curve.png', dpi=150)
plt.close()

# Modelo final baseline com n=10 (como no script original)
modelo_linear = LinearRegression()
selector = RFE(modelo_linear, n_features_to_select=10, step=1)
selector = selector.fit(X_train_sc, y_train)
mask = selector.support_
features = X_train_sc.columns
sel_features_10 = features[mask]
X_sel_10 = X_train_sc[sel_features_10]

score_cv_10 = cross_val_score(modelo_linear, X_sel_10, y_train, cv=10, scoring='r2')
print('R2 CV (n=10, fixo do script original):', np.mean(score_cv_10))

modelo_linear.fit(X_sel_10, y_train)

from sklearn.metrics import mean_squared_error, mean_absolute_error
y_pred = modelo_linear.predict(X_test_sc[sel_features_10])
r2_test = modelo_linear.score(X_test_sc[sel_features_10], y_test)
rmse_test = mean_squared_error(y_test, y_pred) ** 0.5
mae_test = mean_absolute_error(y_test, y_pred)

print('=== BASELINE (script original, n=10 features fixas) ===')
print('Features selecionadas:', list(sel_features_10))
print('R2 teste:', r2_test)
print('RMSE teste:', rmse_test)
print('MAE teste:', mae_test)

with open('elt579/aula2/relatorio_outputs/baseline_resultados.txt', 'w', encoding='utf-8') as f:
    f.write('Melhor n (curva RFE): {}  R2 CV = {:.4f}\n'.format(best_n, max(lista_score)))
    f.write('R2 CV (n=10 fixo): {:.4f}\n'.format(np.mean(score_cv_10)))
    f.write('Features (n=10): {}\n'.format(list(sel_features_10)))
    f.write('R2 teste: {:.4f}\n'.format(r2_test))
    f.write('RMSE teste: {:.4f}\n'.format(rmse_test))
    f.write('MAE teste: {:.4f}\n'.format(mae_test))

# Gráfico de dispersão real vs previsto - baseline
plt.figure(figsize=(5.5, 5.5))
plt.scatter(y_test, y_pred, alpha=0.7, edgecolor='k')
lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
plt.plot(lims, lims, 'r--', label='y = x (predicao perfeita)')
plt.xlabel('Severidade Real')
plt.ylabel('Severidade Prevista')
plt.title('Baseline - Real vs. Previsto (Regressao Linear, teste)')
plt.legend()
plt.tight_layout()
plt.savefig('elt579/aula2/relatorio_outputs/02_baseline_real_vs_previsto.png', dpi=150)
plt.close()
