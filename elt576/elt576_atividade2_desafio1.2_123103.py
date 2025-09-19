# ELT576 - Prática 2 - Desafio 1.2
# Nome: Elmer Antonio Moreira Rodrigues
# Matrícula: 123103 

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq, fftshift
from matplotlib import pyplot as plt
import sounddevice as sd   # biblioteca para tocar áudio

Fs = 10000 # frequencia de amostragem
t = np.arange(0,3,1/Fs)
f0 =  150
t1 = 3
f1 = 450
B = (f1-f0)/t1
y = np.cos(2*np.pi*(f0*t*B/2*np.power(t,2)))
Y = np.absolute(fft(y))
freq = fftfreq(len(y),1/Fs)[0:len(y)//2]

# FFT (só para visualização, opcional)
Y = np.absolute(fft(y))
freq = fftfreq(len(y),1/Fs)[0:len(y)//2]

# plot do sinal y no tempo
plt.plot(t,y)
plt.xlim(0, 0.2) # limites para conseguir ver a senoide
plt.xlabel('Tempo (s)')
plt.ylabel('y(t)')
plt.show()

plt.figure()
plt.plot(freq,Y[0:len(Y)//2])
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")
plt.show()


# ---- TOCAR O ÁUDIO ----
# Normaliza para evitar distorção
y = y.astype(np.float32)
y = y / np.max(np.abs(y))

duracao = len(y) / Fs
print(f"Duração do áudio: {duracao:.3f} segundos")

sd.play(y, Fs)
sd.wait()  # espera terminar a reprodução


