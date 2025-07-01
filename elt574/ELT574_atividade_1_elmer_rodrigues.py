### Aluno: Elmer A. M. Rodrigues
### Turma: ELT 574 2025/1 T1 - ELT 574 - APRENDIZADO DE MÁQUINA
### Questionário Avaliativo 1

import pandas as pd
from scipy.stats import pearsonr

# Caminho para o arquivo CSV (ajuste para o seu caminho local)
file_path = "data/melb_data.csv"

# Leitura do dataset
df = pd.read_csv(file_path)

# Tratamento de nulos para as variáveis que vamos usar
df = df.dropna(subset=['Bedroom2', 'Rooms', 'Price'])

# Criar a nova variável: Proporção de Quartos por Cômodos
df['Quartos_por_Comodo'] = df['Bedroom2'] / df['Rooms']

# Calcular a correlação com o preço (Price)
corr, p_value = pearsonr(df['Quartos_por_Comodo'], df['Price'])

print("Coeficiente de correlação de Pearson entre 'Quartos_por_Comodo' e 'Price':", corr)
print("p-valor:", p_value)

