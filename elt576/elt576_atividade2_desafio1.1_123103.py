# ELT576 - Prática 2 - Desafio 1.1
# Nome: Elmer Antonio Moreira Rodrigues
# Matrícula: 123103 
from matplotlib import pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq, irfft

import numpy as np

Fs = 8000 # frequencia de amostragem
L = 10000 # tamanho do vetor de frequencias

t = np.arange(0, (L-1)/Fs, 1/Fs) # declaracao do vetor de tempo
x = 0.7*np.sin(2 * np.pi * 500 * t) #+ 1*np.sin(2 * np.pi * 2000 * t) + 2*np.random.normal(0,1,L-1) # sinal que iremos analisar


plt.plot(t,x)
plt.xlim(0, 0.005) # limites para conseguir ver os detalhes do sinal
plt.xlabel('Tempo (s)')
plt.show()
X = fft(x)

xf = fftfreq(L-1, 1/Fs) # L-1 por causa do indice 0
plt.plot(xf,np.absolute(X))
plt.xlabel("Freq (Hz)")
plt.ylabel("|X|")
plt.show()

# normalmente, somente a parte positiva das frequencias e plotada
xf_pos = fftfreq(L, 1/Fs)[0:L//2]


fig, axs = plt.subplots(1,2,sharey=True)
fig.set_figwidth(15)
axs[0].plot(xf,np.absolute(X))
axs[0].set_xlabel("Freq (Hz)")
axs[0].set_ylabel("|X|")
axs[0].set_title("fft simétrica")

axs[1].plot(xf_pos,np.absolute(X[0:L//2]))
axs[1].set_xlabel("Freq (Hz)")
axs[1].set_title("fft simétrica freq. positivas")
# axs[1].set_ylim(0, 1)

plt.show()

# transformada inversa de fourier para reconstrucao do sinal
x_new = irfft(X, n=len(t))

plt.plot(t,x, label='x')
plt.plot(t,x_new, "--", label='x irfft')
plt.legend()
plt.xlabel('Tempo (s)')
plt.ylabel('Sinal')
plt.xlim(0, 0.01) # limites para conseguir ver a senoide
plt.show()