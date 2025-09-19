import numpy as np
import matplotlib.pyplot as plt

# 1. Resposta ao impulso do sistema
h = np.concatenate(([1], np.zeros(20), [0.5], np.zeros(10)))

# 2. Entrada no sistema
x = np.concatenate(([0], np.arange(1, 11), np.ones(5)*5, np.zeros(10)))

# 3. Convolução entre x e h
y = np.convolve(x, h)

# Plotando
plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.stem(h)
plt.title("Resposta ao Impulso h[n]")
plt.xlabel("n")
plt.ylabel("h[n]")

plt.subplot(3, 1, 2)
plt.stem(x)
plt.title("Entrada x[n]")
plt.xlabel("n")
plt.ylabel("x[n]")

plt.subplot(3, 1, 3)
plt.stem(y)
plt.title("Saída y[n] = x[n] * h[n]")
plt.xlabel("n")
plt.ylabel("y[n]")

plt.tight_layout()
plt.show()
