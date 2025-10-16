# ELT576 - Prática 2 - Desafio 4
# Nome: Elmer Antonio Moreira Rodrigues
# Matrícula: 123103 

import os
from scipy.io import wavfile
import sounddevice as sd
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt




# importando a biblioteca para ler um arquivo .wav
from scipy.io import wavfile

def play_audio(audio, rate):
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32) / np.max(np.abs(audio))
    sd.play(audio, rate)
    sd.wait()

# pega o diretório onde está este script
base_dir = os.path.dirname(os.path.abspath(__file__))




fs = 2048 # frequencia de amostragem (sintética para o sinal gerado, não relacionada ao arquivo WAV)
t = np.linspace(0, 5, int(fs*5)+1) # garante o número correto de amostras para síntese de áudio
s = np.sin(2*np.pi*262*t) # sinal sintetizado, frequência 262 Hz (Dó central - C4)

plt.figure()
plt.stem(t,s)
plt.title('Sinal de interesse')
plt.xlabel('Tempo (s)')
plt.xlim(0,.05)
plt.show()

ruidoPath = os.path.join(base_dir, "data", "ruido.txt")

# lendo o arquivo ruido.txt
with open(ruidoPath, "r", encoding="utf-8-sig") as arquivo:
    ruido_txt = arquivo.read()
    ruidos = ruido_txt.split()
    ruido = [float(ruido) for ruido in ruidos]

x = s + ruido

# plot do sinal
plt.figure()
plt.stem(t,x) # sinal com ruido
#plt.stem(t,s, linefmt=':') # sinal de interesse
plt.title('Sinal de interesse')
plt.xlabel('Tempo (s)')
plt.xlim(0,.04)
plt.ylim(-40,40)
plt.show()


nperseg = 1024
overlap = 0.5
f, Pxx_den = signal.welch(x, fs,  nperseg=nperseg, noverlap=np.uint8(np.round(nperseg*overlap)))
f0, Pxx_den0 = signal.welch(s, fs,  nperseg=nperseg, noverlap=np.uint8(np.round(nperseg*overlap)))

plt.figure()
plt.plot(f,Pxx_den, label='Sinal com ruído')
plt.plot(f0,Pxx_den0, 'g', label='Sinal puro')
plt.title('Espectro do sinal + ruído')
plt.xlabel('Frequência (Hz)')
plt.legend()
plt.show()

# configuracao dos parametros do filtro butterworth
f1 = 260
f2 = 264

n = 4

# ajustando o filtro butterworth de ordem n e banda de passagem f1 e f2
# "b": numerador
# "a": denominador
b, a = signal.butter(n, [f1, f2], btype='bandpass', output='ba', fs=fs)

# efeito da ordem do filtro na resposta do ganho por frequencia

# configuracao dos parametros do filtro butterworth
f1 = 260
f2 = 264

fig, ax = plt.subplots(1,2)
#ax[1].plot(t,x,'r', label='Sinal com ruído')
fig.set_figwidth(20)


for n in [1, 2, 3, 4, 5, 6]:
    #n = 4

    # ajustando o filtro butterworth de ordem n e banda de passagem f1 e f2
    # "b": numerador
    # "a": denominador
    b, a = signal.butter(n, [f1, f2], btype='bandpass', output='ba', fs=fs)

    # resposta em frequencia do filtro projetado
    # w: frequencias da resposta
    # h: saida do filtro para determinada frequencia (em dominio complexo)
    w, h = signal.freqz(b, a, fs = fs)

    # filtrando o sinal com o filtro de ordem n selecionado
    y = signal.filtfilt(b, a, x)

    ax[0].plot(w, 20 * np.log10(abs(h)), label=f'n={n}')

    # plotando o sinal com filtro e sem filtro
    ax[1].plot(t,y, label=f'n={n}')

ax[0].set_title('Resposta do ganho do filtro digital')
ax[0].set_ylabel('Amplitude (dB)')
ax[0].set_xlabel('Frequência (Hz)')
# ax[0].set_xlim(240,280)
# ax[0].set_ylim(-200,10)
ax[0].grid()
ax[0].legend()
#ax[0].set_legend()

ax[1].set_title('Sinais de interesse filtrados')
ax[1].set_xlabel('Tempo (s)')
ax[1].set_xlim(0.01,0.02)
ax[1].set_ylim(-1.1, 1.1)
ax[1].legend()

plt.grid()
plt.show()

# resposta em frequencia do filtro projetado
# w: frequencias da resposta
# h: saida do filtro para determinada frequencia (em dominio complexo)
w, h = signal.freqz(b, a, fs = fs)

fig, ax1 = plt.subplots()
ax1.set_title('Resposta do ganho do filtro digital')
ax1.plot(w, 20 * np.log10(abs(h)), 'b')
ax1.set_ylabel('Amplitude (dB)', color='b')
ax1.set_xlabel('Frequência (Hz)')
#ax1.set_xlim(240,280)
plt.grid()
plt.show()

# plotando o sinal com filtro e sem filtro
plt.figure()
plt.plot(t,x,'r', label='Sinal com ruído')
plt.plot(t,y,'b', label='Sinal filtrado')
plt.xlabel('Tempo (s)')
plt.legend()
plt.xlim(0,0.04)
plt.show()