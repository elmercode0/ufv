# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RS = 0  # mesma semente do script original, para comparacao justa

df = pd.read_csv('elt579/aula2/dataset_problema2.csv')
X = df.drop(['id', 'Severidade'], axis=1)
y = df['Severidade']

# ------------------------------------------------------------------
# 1) Analise de correlacao entre as features (multicolinearidade)
# ------------------------------------------------------------------
plt.figure(figsize=(10, 8))
corr = X.corr()
im = plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(im, label='Correlacao de Pearson')
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title('Matriz de Correlacao entre as Features (indices de vegetacao)')
plt.tight_layout()
plt.savefig('elt579/aula2/relatorio_outputs/03_matriz_correlacao.png', dpi=150)
plt.close()

alta_corr = (corr.abs() > 0.9).sum().sum() - len(corr)
print('Pares de features com |correlacao| > 0.9 (contando duplicado):', alta_corr)

# ------------------------------------------------------------------
# 2) Split e padronizacao (identico ao script original)
# ------------------------------------------------------------------
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RS)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_sc = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test_sc = pd.DataFrame(scaler.transform(X_test), columns=X_train.columns)

# ------------------------------------------------------------------
# 3) Comparacao de varios algoritmos de regressao (todas as features)
# ------------------------------------------------------------------
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, KFold

cv = KFold(n_splits=10, shuffle=True, random_state=RS)

modelos = {
    'Regressao Linear': LinearRegression(),
    'Ridge': Ridge(alpha=1.0, random_state=RS),
    'Lasso': Lasso(alpha=0.1, random_state=RS),
    'ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=RS),
    'KNN Regressor': KNeighborsRegressor(n_neighbors=5),
    'SVR (RBF)': SVR(kernel='rbf', C=10, epsilon=0.5),
    'Random Forest': RandomForestRegressor(n_estimators=300, random_state=RS),
    'Gradient Boosting': GradientBoostingRegressor(random_state=RS),
}

resultados_modelos = {}
for nome, modelo in modelos.items():
    scores = cross_val_score(modelo, X_train_sc, y_train, cv=cv, scoring='r2')
    resultados_modelos[nome] = scores.mean()
    print(f'{nome:20s} R2 CV = {scores.mean():.4f} (+/- {scores.std():.4f})')

plt.figure(figsize=(9, 5))
nomes = list(resultados_modelos.keys())
valores = list(resultados_modelos.values())
cores = ['#4c72b0' if v == max(valores) else '#8c9ec0' for v in valores]
plt.bar(nomes, valores, color=cores)
plt.axhline(0.8656, color='red', linestyle='--', label='Baseline (LinearRegression + RFE-10) = 0.8656')
plt.ylabel('R2 medio (CV = 10, todas as 20 features)')
plt.title('Comparacao de Algoritmos de Regressao')
plt.xticks(rotation=30, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('elt579/aula2/relatorio_outputs/04_comparacao_modelos.png', dpi=150)
plt.close()

melhor_nome = max(resultados_modelos, key=resultados_modelos.get)
print('Melhor modelo (todas as features):', melhor_nome, resultados_modelos[melhor_nome])

# ------------------------------------------------------------------
# 4) RFE com o melhor estimador linear (Ridge) - curva do numero de features
#    Ridge é mais estável que LinearRegression pura sob multicolinearidade
# ------------------------------------------------------------------
from sklearn.feature_selection import RFE

max_f = 20
lista_score_ridge = []
for i in range(1, max_f + 1):
    ridge = Ridge(alpha=1.0, random_state=RS)
    selector = RFE(ridge, n_features_to_select=i, step=1)
    selector.fit(X_train_sc, y_train)
    sel = X_train_sc.columns[selector.support_]
    score = cross_val_score(ridge, X_train_sc[sel], y_train, cv=cv, scoring='r2')
    lista_score_ridge.append(score.mean())

best_n_ridge = int(np.argmax(lista_score_ridge)) + 1
print('Melhor n de features (RFE + Ridge):', best_n_ridge, 'R2 CV =', max(lista_score_ridge))

plt.figure(figsize=(7, 4.5))
plt.plot(range(1, max_f + 1), lista_score_ridge, marker='o', label='RFE + Ridge')
plt.axvline(best_n_ridge, color='red', linestyle='--', alpha=0.6, label=f'melhor n={best_n_ridge}')
plt.xlabel('Numero de features selecionadas (RFE)')
plt.ylabel('R2 medio (CV=10)')
plt.title('Selecao de Features com RFE + Ridge')
plt.legend()
plt.tight_layout()
plt.savefig('elt579/aula2/relatorio_outputs/05_rfe_ridge_curve.png', dpi=150)
plt.close()

# ------------------------------------------------------------------
# 5) Hiperparametros - GridSearchCV no Ridge (alpha) usando as features do melhor RFE
# ------------------------------------------------------------------
from sklearn.model_selection import GridSearchCV

ridge_final = Ridge(random_state=RS)
selector_final = RFE(ridge_final, n_features_to_select=best_n_ridge, step=1)
selector_final.fit(X_train_sc, y_train)
sel_features_final = X_train_sc.columns[selector_final.support_]
X_sel_final = X_train_sc[sel_features_final]

param_grid = {'alpha': [0.001, 0.01, 0.1, 0.5, 1, 2, 5, 10, 20, 50, 100]}
grid = GridSearchCV(Ridge(random_state=RS), param_grid, cv=cv, scoring='r2')
grid.fit(X_sel_final, y_train)

print('Melhor alpha (Ridge):', grid.best_params_, 'R2 CV =', grid.best_score_)

plt.figure(figsize=(7, 4.5))
alphas = param_grid['alpha']
scores_alpha = grid.cv_results_['mean_test_score']
plt.plot(alphas, scores_alpha, marker='o')
plt.xscale('log')
plt.axvline(grid.best_params_['alpha'], color='red', linestyle='--',
            label=f"melhor alpha={grid.best_params_['alpha']}")
plt.xlabel('alpha (regularizacao, escala log)')
plt.ylabel('R2 medio (CV=10)')
plt.title('GridSearchCV - Ajuste do hiperparametro alpha (Ridge)')
plt.legend()
plt.tight_layout()
plt.savefig('elt579/aula2/relatorio_outputs/06_gridsearch_alpha.png', dpi=150)
plt.close()

# ------------------------------------------------------------------
# 6) Modelo final melhorado: Ridge com alpha otimo + features do RFE
# ------------------------------------------------------------------
from sklearn.metrics import mean_squared_error, mean_absolute_error

modelo_melhorado = Ridge(alpha=grid.best_params_['alpha'], random_state=RS)
modelo_melhorado.fit(X_sel_final, y_train)

y_pred_melhorado = modelo_melhorado.predict(X_test_sc[sel_features_final])
r2_melhorado = modelo_melhorado.score(X_test_sc[sel_features_final], y_test)
rmse_melhorado = mean_squared_error(y_test, y_pred_melhorado) ** 0.5
mae_melhorado = mean_absolute_error(y_test, y_pred_melhorado)

print('=== MODELO MELHORADO (Ridge + RFE + GridSearchCV) ===')
print('Features selecionadas:', list(sel_features_final))
print('R2 teste:', r2_melhorado)
print('RMSE teste:', rmse_melhorado)
print('MAE teste:', mae_melhorado)

with open('elt579/aula2/relatorio_outputs/melhorado_resultados.txt', 'w', encoding='utf-8') as f:
    f.write('Comparacao de modelos (CV=10, todas features):\n')
    for nome, v in sorted(resultados_modelos.items(), key=lambda kv: -kv[1]):
        f.write(f'  {nome}: {v:.4f}\n')
    f.write('\nMelhor n features (RFE+Ridge): {}  R2 CV = {:.4f}\n'.format(best_n_ridge, max(lista_score_ridge)))
    f.write('Melhor alpha (GridSearchCV): {}  R2 CV = {:.4f}\n'.format(grid.best_params_['alpha'], grid.best_score_))
    f.write('Features finais: {}\n'.format(list(sel_features_final)))
    f.write('R2 teste: {:.4f}\n'.format(r2_melhorado))
    f.write('RMSE teste: {:.4f}\n'.format(rmse_melhorado))
    f.write('MAE teste: {:.4f}\n'.format(mae_melhorado))

# Grafico real vs previsto - melhorado
plt.figure(figsize=(5.5, 5.5))
plt.scatter(y_test, y_pred_melhorado, alpha=0.7, edgecolor='k', color='seagreen')
lims = [min(y_test.min(), y_pred_melhorado.min()), max(y_test.max(), y_pred_melhorado.max())]
plt.plot(lims, lims, 'r--', label='y = x (predicao perfeita)')
plt.xlabel('Severidade Real')
plt.ylabel('Severidade Prevista')
plt.title('Modelo Melhorado - Real vs. Previsto (Ridge, teste)')
plt.legend()
plt.tight_layout()
plt.savefig('elt579/aula2/relatorio_outputs/07_melhorado_real_vs_previsto.png', dpi=150)
plt.close()

# Grafico comparativo final baseline x melhorado
plt.figure(figsize=(7, 4.5))
metricas = ['R2 (teste)', 'RMSE (teste)', 'MAE (teste)']
baseline_vals = [0.8876, 7.5395, 6.3441]
melhorado_vals = [r2_melhorado, rmse_melhorado, mae_melhorado]

x = np.arange(len(metricas))
w = 0.35
plt.bar(x - w/2, baseline_vals, width=w, label='Baseline (script original)', color='#8c9ec0')
plt.bar(x + w/2, melhorado_vals, width=w, label='Modelo melhorado (Ridge+RFE+GridSearch)', color='#4c72b0')
plt.xticks(x, metricas)
plt.title('Comparacao Final: Baseline x Modelo Melhorado (conjunto de teste)')
plt.legend()
for i, (b, m) in enumerate(zip(baseline_vals, melhorado_vals)):
    plt.text(i - w/2, b, f'{b:.2f}', ha='center', va='bottom', fontsize=8)
    plt.text(i + w/2, m, f'{m:.2f}', ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.savefig('elt579/aula2/relatorio_outputs/08_comparacao_final.png', dpi=150)
plt.close()
