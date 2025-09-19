# ELT576 - Prática 2 - Desafio 2
# Nome: Elmer Antonio Moreira Rodrigues
# Matrícula: 123103 

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq, fftshift
from matplotlib import pyplot as plt
import sounddevice as sd   # biblioteca para tocar áudio

# declarando o sinal e calculando os pontos do espectrograma
Fs = 100000
t = np.arange(0,3,1/Fs) # alterei o tempo para 3 segundos
f0 =  150
t1 = 3
f1 = 450
B = (f1-f0)/t1
# y = np.cos(2*np.pi*(f0*t*B/2*np.power(t,2)))
y = 0.7*np.sin(2 * np.pi * 500 * t) + 2*np.sin(2 * np.pi * 2000 * t) + np.cos(2*np.pi*(f0*t*B/2*np.power(t,2)))
f, t, Sxx = signal.spectrogram(y, Fs)

# plotando o espectrograma para as frequencias positivas
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequência (Hz)')
plt.xlabel('Tempo (s)')
plt.colorbar(label='Energia')
# plt.xlim(0.4,0.45)
plt.show()


# ---- TOCAR O ÁUDIO ----
# Normaliza para evitar distorção
y = y.astype(np.float32)
y = y / np.max(np.abs(y))

duracao = len(y) / Fs
print(f"Duração do áudio: {duracao:.3f} segundos")

sd.play(y, Fs)
sd.wait()  # espera terminar a reprodução


