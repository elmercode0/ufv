# Atividade Aberta 1
# Aluno: Elmer Antônio Moreira Rodrigues


# Exercício 1
print("\n###  Exercício 1 ###")

a = 13
b = 18
c = b - a
d = a + c
e = b - c

print("b - a = ", c)
print("a + c = ", d)
print("b - c = ", e)
print("a > b:", a > b)
print("d < b:", d < b)
print("d == e:", d == e)
print("a != a:", a != a)
print("a >= d:", a >= d)
print("d <= e:", d <= e)

#Exercício 2
print("\n###  Exercício 2 ###")

a = 5
b = 2
c = b * a
d = a * a
e = b * b

print("b * a = ", c)
print("a * a = ", d)
print("b * b = ", e)
print("d > e:", d > e)
print("d < e:", d < e)
print("d == (a * a):", d == (a * a))
print("(d * b) != (e * a):", (d * b) != (e * a))
print("a >= c:", a >= c)
print("c <= e:", c <= e)

#Exercício 3
print("\n###  Exercício 3 ###")
x = 64

while x > 2:
    print(x)
    x = int(x / 2)

#Exercício 4
print("\n###  Exercício 4 ###")
nota = int(input("digite uma nota entre 0 e 100: "))

while nota > 100 or nota < 0:
    print("nota invalida!")
    nota = int(input("digite uma nota entre 0 e 100: "))

if nota < 60:
    print("aluno reprovado")
else:
    print("aluno aprovado")