path = "c:/code/ufv/elt576/img/lua.jpg"

import numpy as np
from PIL import Image
from scipy.signal import convolve2d
import matplotlib.pyplot as plt

# 1. Carregar a imagem em escala de cinza
I = Image.open(path).convert("L")  # "L" = grayscale
I = np.array(I)

# 2. Definir o kernel Laplaciano (filtro de realce)
F = np.array([[-1, -1, -1],
              [-1,  8, -1],
              [-1, -1, -1]])

# 3. Convoluir o kernel com a imagem
I_conv = convolve2d(I, F, mode="same", boundary="symm")

# 4. Somar imagem original + convoluída para realce
I_realce = I + I_conv

# 5. Normalizar para 0–255
I_conv = np.clip(I_conv, 0, 255).astype(np.uint8)
I_realce = np.clip(I_realce, 0, 255).astype(np.uint8)

# 6. Exibir resultados
plt.figure(figsize=(15,5))

plt.subplot(1,3,1)
plt.imshow(I, cmap="gray")
plt.title("Imagem Original")
plt.axis("off")

plt.subplot(1,3,2)
plt.imshow(I_conv, cmap="gray")
plt.title("Imagem Após Convolução (Detalhes)")
plt.axis("off")

plt.subplot(1,3,3)
plt.imshow(I_realce, cmap="gray")
plt.title("Imagem Realçada (Original + Convolução)")
plt.axis("off")

plt.tight_layout()
plt.show()
