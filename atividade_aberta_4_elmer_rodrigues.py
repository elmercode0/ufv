import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/Exercicio Aberto 4.csv')

# a. Média das idades dos compradores
media_idade = df['Idade'].mean()
print(f"Média das idades: {media_idade:.2f} anos") #media de idade dos compradores
### Saída ### 
# Média das idades: 25.78 anos

# b. Comprador mais novo
comprador_mais_novo = df.loc[df['Idade'].idxmin()] #identifica o comprador mais novo
print("\nComprador mais novo:") 
print(f"Idade: {comprador_mais_novo['Idade']}") # alguns compradores não tem idade inserida
print(f"Nome do Produto: {comprador_mais_novo['Nome do Produto']}")
print(f"Localização: {comprador_mais_novo['Localização']}")
print(f"Tipo de Pagamento: {comprador_mais_novo['Tipo de Pagamento']}") 
### SAÍDA ### 

# Comprador mais novo:
# Idade: 0.0
# Nome do Produto: Mentoria Apollo 11
# Localização: GOIÁS
# Tipo de Pagamento: Pix

# b. Comprador mais velho
comprador_mais_velho = df.loc[df['Idade'].idxmax()] #identifica o comprador mais velho
print("\nComprador mais velho:")
print(f"Idade: {comprador_mais_velho['Idade']}")
print(f"Nome do Produto: {comprador_mais_velho['Nome do Produto']}")
print(f"Localização: {comprador_mais_velho['Localização']}")
print(f"Tipo de Pagamento: {comprador_mais_velho['Tipo de Pagamento']}")
### SAÍDA ### 
# Comprador mais velho:
# Idade: 60.0
# Nome do Produto: Mentoria Apollo 11
# Localização: Distrito Federal
# Tipo de Pagamento: Boleto


# c. Produto com mais vendas
produto_mais_vendido = df['Nome do Produto'].value_counts().idxmax()
quantidade_mais_vendido = df['Nome do Produto'].value_counts().max()
print(f"\nProduto com mais vendas: {produto_mais_vendido} ({quantidade_mais_vendido} vendas)")
### SAÍDA ### 
# Produto com mais vendas: Mentoria Apollo 11 (248 vendas)

# Conta a frequência de cada tipo de pagamento
pagamentos = df['Tipo de Pagamento'].value_counts()

# Cria o gráfico de barras
plt.figure(figsize=(8, 5))
pagamentos.plot(kind='bar', title='Métodos de Pagamento Mais Utilizados')
plt.xlabel('Tipo de Pagamento')
plt.ylabel('Quantidade de Compras')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show() # abrindo gráfico
print("\nGráfico de barras com método de pagamento mais utilizado plotado na tela.")


# Converte a coluna de datas para o formato datetime
df['Data de Venda'] = pd.to_datetime(df['Data de Venda'], dayfirst=True)

# Cria uma nova coluna apenas com o mês e ano (ex: 2021-05)
df['Ano-Mes'] = df['Data de Venda'].dt.to_period('M').astype(str)

# Conta quantas vendas ocorreram por mês
vendas_por_mes = df['Ano-Mes'].value_counts().sort_index()

# Gera o gráfico
plt.figure(figsize=(10, 5))
vendas_por_mes.plot(kind='bar', color='skyblue')
plt.title('Quantidade de Vendas por Mês')
plt.xlabel('Ano-Mês')
plt.ylabel('Número de Vendas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()
print("\nGráfico de barras com quantidade de vendas por mês plotado na tela.")

# Conta as vendas por estado (coluna "Localização")
vendas_por_estado = df['Localização'].value_counts().sort_values(ascending=False)

# Cria o gráfico
plt.figure(figsize=(10, 6))
vendas_por_estado.plot(kind='bar', color='mediumseagreen')
plt.title('Quantidade de Vendas por Estado')
plt.xlabel('Estado')
plt.ylabel('Número de Vendas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()
print("\nGráfico de barras com as vendas por estado plotado na tela.")
