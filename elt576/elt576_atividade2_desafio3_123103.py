# ELT576 - Prática 2 - Desafio 3
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

# monta o caminho até a pasta data relativa ao projeto
soundPath = os.path.join(base_dir, "data", "lena.wav")

# lê o arquivo wav
samplerate, lena = wavfile.read(soundPath)

print(f"Taxa de amostragem: {samplerate} Hz")
print(f"Duração: {len(lena)/samplerate:.2f} segundos")


# Tocar o áudio
#play_audio(lena, samplerate)


# extraindo o espectrograma
f, t, Sxx = signal.spectrogram(lena, samplerate)


# plotando o espectrograma do sinal
plt.pcolormesh(t, f, Sxx, shading='gouraud', cmap='gray')
plt.ylabel('Frequência (Hz)')
plt.xlabel('Tempo (s)')
plt.ylim(0,17500) # so para recortar a parte sem informacao
plt.show()

# variando os tamanhos das amostras por janela
npersegs = [256, 1024, 4096, 8192] # 256 e o valor padrao

fig, ax = plt.subplots(1,len(npersegs),sharey=True)
fig.set_figwidth(20)
fig.set_figheight(5)

for index, nperseg in enumerate(npersegs):

  # extraindo o espectrograma
  f2, t2, Sxx2 = signal.spectrogram(lena, samplerate,
                                #window=('tukey', 0.25),
                                nperseg=nperseg,
                                noverlap=None,
                                nfft=None)

  # plotando o espectrograma do sinal
  ax[index].pcolormesh(t2, f2, Sxx2, shading='gouraud', cmap='gray')
  ax[index].set_ylabel('Frequência (Hz)')
  ax[index].set_xlabel('Tempo (s)')
  ax[index].set_title(f'Pontos por janela: {nperseg}')
  ax[index].set_ylim(0,17500) # so para recortar a parte sem informacao

plt.show()

# variando os pontos em sobreposicao entre as janelas
noverlaps = [2, 4, 8, 16, 32, 64]

fig, ax = plt.subplots(len(npersegs),len(noverlaps),sharey=True,sharex=True)
fig.set_figwidth(20)
fig.set_figheight(15)

for index1, nperseg in enumerate(npersegs):
  for index2, noverlap in enumerate(noverlaps):
    # extraindo o espectrograma
    f3, t3, Sxx3 = signal.spectrogram(lena, samplerate,
                                  #window=('tukey', 0.25),
                                  nperseg=nperseg,
                                  noverlap=(nperseg // noverlap),
                                  nfft=None)
    # plotando o espectrograma do sinal
    ax[index1, index2].pcolormesh(t3, f3, Sxx3, shading='gouraud', cmap='gray')
    ax[index1, 0].set_ylabel('Frequência (Hz)')
    ax[len(npersegs)-1, index2].set_xlabel('Tempo (s)')
    ax[index1, index2].set_title(f'Tam. janela: {nperseg} \n Sobreposição: {nperseg // noverlap}')
    ax[index1, index2].set_ylim(0,17500) # so para recortar a parte sem informacao

plt.show()

# variando os pontos em sobreposicao entre as janelas
nffts = [1, 2, 4, 8]

fig, ax = plt.subplots(4,len(npersegs),sharey=True,sharex=True)
fig.set_figwidth(15)
fig.set_figheight(15)

freq_limit = 17500

# rows -> nffts multipliers, cols -> npersegs
for row_idx, nfft_mul in enumerate(nffts):
    for col_idx, nperseg in enumerate(npersegs):
        nfft_val = nperseg * nfft_mul

        # extrai espectrograma
        f_spec, t_spec, Sxx_spec = signal.spectrogram(
            lena,
            samplerate,
            nperseg=nperseg,
            noverlap=None,
            nfft=nfft_val,
        )

        ax[row_idx, col_idx].pcolormesh(t_spec, f_spec, Sxx_spec, shading='gouraud', cmap='gray')

        # rótulos apenas nas bordas para evitar repetição
        if col_idx == 0:
            ax[row_idx, col_idx].set_ylabel('Frequência (Hz)')
        if row_idx == len(nffts) - 1:
            ax[row_idx, col_idx].set_xlabel('Tempo (s)')

        ax[row_idx, col_idx].set_title(f'Janela: {nperseg}\n nfft: {nfft_val}')
        ax[row_idx, col_idx].set_ylim(0, freq_limit)

fig.tight_layout()
plt.show()