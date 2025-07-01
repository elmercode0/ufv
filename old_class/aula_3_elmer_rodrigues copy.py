# Atividade Aberta 3
# Aluno: Elmer Antônio Moreira Rodrigues

import numpy as np

#notas = np.empty(5)
#notas = np.zeros(5, dtype=int)
#notas = np.array([4,3,2,1])
#print("notas:", notas)

# n = int(input('Informe o número de elementos: '))
# A= np.empty(n)

# for i in range(0, n):
#     A[i] = float(input('Informe o %dº elemento: ' % (i+1)))

# for i in range(0, n):
#    A[i] = A[i] * 3

# print('Imprimindo vetor na tela...')

# for i in range(0,n):
#     print('%5.2f' % A[i], end=' | ')

# print()

# matriz = np.zeros((3,3))

# print(matriz)

from car import Car

newCar = Car('audi', 'a4', 2019)
print(newCar.get_descriptive_name())

newCar.increment_odometer(1111)

newCar.read_odometer()