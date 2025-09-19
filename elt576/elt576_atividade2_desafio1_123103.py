path = "c:/code/ufv/elt576/img/texto.jpg"
import numpy as np
from PIL import Image
from scipy.signal import convolve2d
import matplotlib.pyplot as plt

# 1. Carregar a imagem em escala de cinza
I = Image.open(path).convert("L")  # "L" = grayscale
I = np.array(I)

# 2. Definir o kernel fornecido
F = (1/9) * np.array([[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 2]])

# 3. Aplicar convolução 2D
I_conv = convolve2d(I, F, mode='same', boundary='symm')

# 4. Normalizar para 0-255
I_conv = np.clip(I_conv, 0, 255).astype(np.uint8)

# 5. Mostrar resultados
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(I, cmap='gray')
plt.title("Imagem Original")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(I_conv, cmap='gray')
plt.title("Imagem Filtrada")
plt.axis("off")

plt.tight_layout()
plt.show()
