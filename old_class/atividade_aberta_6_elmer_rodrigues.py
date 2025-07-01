### Aluno: Elmer A. M. Rodrigues
### Turma: 2025/1 - ELT 573 2025/1 T1 - INTRODUÇÃO AO APRENDIZADO ESTATÍSTICO
### Atividade avaliativa 06 – Relatórios (2025/1)

import numpy as np
import pandas as pd
import urllib.request
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr

# Carregar o dataset Boston Housing
url = "https://lib.stat.cmu.edu/datasets/boston"
response = urllib.request.urlopen(url)
data_raw = response.read().decode('utf-8')
data_lines = data_raw.split('\n')[22:]

data_values = []
for i in range(0, len(data_lines) - 1, 2):
    line1 = data_lines[i].strip().split()
    line2 = data_lines[i + 1].strip().split()
    if line1 and line2:
        data_values.append(line1 + line2)

data_np = np.array(data_values, dtype=float)
columns = [
    'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM',
    'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV'
]
df = pd.DataFrame(data_np, columns=columns)

# Definir variáveis independentes (X) e dependente (y)
X = df.drop('MEDV', axis=1).values
y = df['MEDV'].values

# Modelos a comparar
models = {
    'Regressão Linear': LinearRegression(),
    'Árvore de Regressão': DecisionTreeRegressor(random_state=42),
    'Bagging': BaggingRegressor(random_state=42),
    'Random Forest': RandomForestRegressor(random_state=42)
}

# Leave-One-Out Cross Validation
loo = LeaveOneOut()
results = {}

for name, model in models.items():
    y_pred = np.zeros_like(y)
    for train_idx, test_idx in loo.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        model.fit(X_train, y_train)
        y_pred[test_idx] = model.predict(X_test)
    
    mse = mean_squared_error(y, y_pred)
    corr, _ = pearsonr(y, y_pred)
    results[name] = {'MSE': mse, 'Correlação': corr}

# Exibir resultados
report = pd.DataFrame(results).T
print("\n=== Comparação entre os Modelos ===")
print(report)

