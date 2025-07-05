### Aluno: Elmer A. M. Rodrigues
### Turma: ELT 574 2025/1 T1 - ELT 574 - APRENDIZADO DE MÁQUINA
### Questionário Avaliativo 1

import pandas as pd

# Carregar os dados
file_path = 'data/melb_data.csv'  # Altere se necessário
df = pd.read_csv(file_path)

# Verificar número de famílias (linhas)
num_familias = df.shape[0]
print(f"Número de famílias (linhas no dataset): {num_familias}")

# Preencher valores ausentes em 'Rooms' e 'Bedroom2' para evitar erros
df['Rooms'] = df['Rooms'].fillna(0)
df['Bedroom2'] = df['Bedroom2'].fillna(0)

# Criar variável derivada: total de cômodos (quartos + comodos adicionais)
df['Total_comodos'] = df['Rooms'] + df['Bedroom2']

# Calcular o coeficiente de correlação linear com a variável alvo 'Price'
correlacao = df[['Total_comodos', 'Price']].corr().iloc[0, 1]

print(f"Coeficiente de correlação linear entre 'Total_comodos' e 'Price': {correlacao:.2f}")

print("\nInterpretação da correlação:")

# Análise da correlação
if abs(correlacao) < 0.1:
    print("→ Correlação desprezível ou nula.")
    print("Não há relação linear entre o número total de cômodos e o preço do imóvel.")
elif abs(correlacao) < 0.3:
    print("→ Correlação fraca.")
    print("Existe uma leve tendência de relação entre total de cômodos e preço, mas não é significativa.")
elif abs(correlacao) < 0.5:
    print("→ Correlação moderada.")
    print("Há uma tendência moderada de que imóveis com mais cômodos tenham preços maiores.")
elif abs(correlacao) < 0.7:
    print("→ Correlação moderadamente forte.")
    print("Existe uma relação linear clara entre total de cômodos e o preço do imóvel.")
elif abs(correlacao) < 0.9:
    print("→ Correlação forte.")
    print("O número total de cômodos é um forte indicador do valor do imóvel.")
else:
    print("→ Correlação muito forte.")
    print("O preço dos imóveis praticamente cresce de forma linear com o número de cômodos.")


