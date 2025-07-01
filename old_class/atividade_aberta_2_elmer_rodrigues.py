# Atividade Aberta 2 
# Aluno: Elmer Antônio Moreira Rodrigues

import numpy as np



# Exercício 1
print("\n###  Exercício 1 ###")

notas = []
for i in range(5):
    nota = float(input(f"Digite a nota {i+1}: "))
    notas.append(nota)

media = sum(notas) / 5

print("Média:", media)

if media >= 60.0:
    print("Aluno aprovado!")
else:
    print("Aluno reprovado!")

# Exercício 2
print("\n###  Exercício 2 ###")
matriz = np.zeros((5, 5), dtype=int)

for i in range(5):
    for j in range(5):
        matriz[i][j] = int(input(f"Digite o valor para a posição ({i},{j}): "))

for i in range(5):
    soma_linha = sum(matriz[i])
    print(f"Soma da linha {i}: {soma_linha}")

# Exercício 3
print("\n###  Exercício 3 ###")
def verificar_negativos(ent1, ent2):
    if (ent1 - ent2) < 0:
        print("ent1 - ent2 é negativo")
    if (ent1 * ent2) < 0:
        print("ent1 * ent2 é negativo")
    if (ent1 + ent2) < 0:
        print("ent1 + ent2 é negativo")

numero1 = int(input("Digite o número 1: "))
numero2 = int(input("Digite o número 2: "))

verificar_negativos(numero1, numero2)


# Exercício 4
print("\n###  Exercício 4 ###")

def substituir_pares(caractere, texto, tamanho):
    nova_string = ""
    for i in range(tamanho):
        if i % 2 == 0:
            nova_string += caractere
        else:
            nova_string += texto[i]
    return nova_string

letra = input("Digite uma letra: ")
palavra = input("Digite uma palavra: ")
resultado = substituir_pares(letra, palavra, len(palavra))
print("Texto substituído pela letra informada: ", resultado)
