# Atividade Aberta 3
# Aluno: Elmer Antônio Moreira Rodrigues

import numpy as np

# Exercício 1 
tupla = (3, 5, 7, 9)               # Cria uma lista com os elementos 3, 5, 7, 9
resultado = tupla[1] + tupla[-1]   # Soma o elemento de índice 1 (5) com o último elemento (9)

print("Resultado = ", resultado)   # Resultado = 14

#Exercício 2
lista = [2, 4, 6, 8, 10]   # Cria uma lista com os elementos 2, 4, 6, 8 e 10
lista.append(12)           # Adiciona o número 12 no final da lista
lista.insert(2, 5)         # Insere o número 5 na posição de índice 2
del lista[4]               # Remove o elemento que está no índice 4

print("Conteúdo da lista:", lista) # Conteúdo da lista: [2, 4, 5, 6, 10, 12]

# Exercício 3
dicionario = {'a': 1, 'b': 2, 'c': 3}   # Cria um dicionário com as chaves 'a', 'b' e 'c' associadas aos valores 1, 2 e 3
dicionario['b'] = dicionario['c'] + 2   # Atualiza o valor da chave 'b' para o valor da chave 'c' (3) + 2, ou seja, 5
dicionario['d'] = 4                     # Adiciona uma nova chave 'd' com valor 4 no dicionário

print("Dicionario: ", dicionario)       # Resultado final do Dicionario:  {'a': 1, 'b': 5, 'c': 3, 'd': 4}

# Exercício 4
numeros = [1, 2, 3, 4, 5, 6]             # Cria uma lista com os números de 1 a 6
resultado = []                           # Cria uma lista vazia para armazenar os resultados

for i in range(len(numeros)):             # Percorre os índices da lista numeros
    if i % 2 == 0:                        # Se o índice for par
        resultado.append(numeros[i] ** 2) # Adiciona o quadrado do número correspondente
    else:                                 # Se o índice for ímpar
        resultado.append(numeros[i] * 2)  # Adiciona o dobro do número correspondente

print("Resultado= ", resultado)            # Imprime a lista resultado: [1, 4, 9, 8, 25, 12]

resultado_final = sum(resultado)          # Calcula a soma de todos os elementos da lista resultado
print("Resultado final= ", resultado_final)  # Imprime o valor da soma final = 59
