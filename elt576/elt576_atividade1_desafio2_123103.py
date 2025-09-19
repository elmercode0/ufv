path = "c:/code/ufv/elt576/data/trumpet.mat"


import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import convolve

# 1. Carregar o arquivo trumpet.mat
data = loadmat(path)
print(data.keys())


# 2. Extrair sinal e frequência
x = data["y"].flatten()         # sinal
Fs = int(data["Fs"].flatten()[0])  # frequência de amostragem

# 3. Criar resposta ao impulso quadrada
h2 = np.concatenate((np.ones(50)/50, np.zeros(20)))

# 4. Convoluir sinal com h2
y2 = convolve(x, h2, mode="full")

# 5. Vetores de tempo
t = np.arange(len(x)) / Fs
t2 = np.arange(len(y2)) / Fs

# 6. Plotar sinais
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, x)
plt.title("Sinal Original (Trumpet)")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.plot(t2, y2)
plt.title("Sinal Filtrado (Convolução com h2)")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()
