# ELT576 - Prática 2 - Desafio 3
# Nome: Elmer Antonio Moreira Rodrigues
# Matrícula: 123103 

import os
import sys
import math
import time
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq, irfft
from scipy import signal
from scipy.io import wavfile, loadmat

# -------------------------- Utilidades --------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

def play_audio(y: np.ndarray, fs: int):
    """Toca o sinal y em fs Hz sem salvar em disco. Silencia se não houver dispositivo."""
    if y is None or len(y) == 0:
        print("Nada para tocar.")
        return
    y = np.asarray(y, dtype=np.float32)
    peak = np.max(np.abs(y)) or 1.0
    y = y / peak
    try:
        sd.play(y, fs)
        sd.wait()
        print("Áudio reproduzido com sucesso.")
    except Exception as e:
        print(f"[Aviso] Não foi possível tocar o áudio ({e}). Prosseguindo sem reprodução.")

def download_if_missing(url: str, dest_path: str):
    """Baixa um arquivo HTTP(S) se não existir localmente."""
    if os.path.exists(dest_path):
        return dest_path
    try:
        print(f"Baixando {os.path.basename(dest_path)} ...")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(r.content)
        print(f"Salvo em {dest_path}")
    except Exception as e:
        print(f"[Aviso] Falha ao baixar {url}: {e}")
        print("Coloque o arquivo manualmente em:", dest_path)
    return dest_path

def seconds_str(n_samples: int, fs: int) -> str:
    return f"{n_samples / fs:.3f} s"

# -------------------------- Desafio 1 --------------------------
def desafio1_tempo_freq():
    """
    1) Tempo <-> Freq (FFT) + reconstrução
    - Sinal: senoides + ruído
    - FFT bruta, centralizada e unilateral
    - IRFFT para reconstrução
    """
    print("\n[Desafio 1] Tempo <-> Freq (FFT) + Reconstrução")
    Fs = 8000
    L  = 10000
    t  = np.arange(0, L/Fs, 1/Fs)

    np.random.seed(42)
    x = (0.7*np.sin(2*np.pi*500*t)
         + 1.0*np.sin(2*np.pi*2000*t)
         + 2.0*np.random.normal(0,1,len(t)))

    # Sinal no tempo (trecho)
    Nplot = 1000
    plt.figure(figsize=(10,3))
    plt.plot(t[:Nplot], x[:Nplot])
    plt.title("x(t) - trecho")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # FFT não centralizada
    X  = fft(x)
    xf = fftfreq(len(x), d=1/Fs)
    plt.figure(figsize=(10,3))
    plt.plot(xf, np.abs(X))
    plt.title("Espectro |X(f)| (não centralizado)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("|X(f)|")
    plt.xlim([-Fs/2, Fs/2])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # FFT centralizada
    Xc  = fftshift(X)
    xfc = fftshift(xf)
    plt.figure(figsize=(10,3))
    plt.plot(xfc, np.abs(Xc))
    plt.title("Espectro |X(f)| (centralizado)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("|X(f)|")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Espectro unilateral (positivas) + escala de magnitude
    Xpos = rfft(x)
    fpos = rfftfreq(len(x), d=1/Fs)
    mag  = (2.0/len(x))*np.abs(Xpos)  # DC/Nyquist fora a fator 2
    plt.figure(figsize=(10,3))
    plt.plot(fpos, mag)
    plt.title("Espectro unilateral (0..Fs/2)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude (2/L · |Xpos|)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Reconstrução no tempo
    x_rec = irfft(Xpos, n=len(x))
    plt.figure(figsize=(10,3))
    plt.plot(t[:Nplot], x[:Nplot], label="x(t) original")
    plt.plot(t[:Nplot], x_rec[:Nplot], "--", label="x_rec(t)")
    plt.title("Comparação no tempo (trecho)")
    plt.xlabel("Tempo (s)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Tocar um tom (opcional): 440 Hz por 1 s
    beep_t = np.arange(0, 1, 1/Fs)
    beep   = 0.3*np.sin(2*np.pi*440*beep_t)
    print("Reproduzindo um tom de 440 Hz (1 s)...")
    play_audio(beep, Fs)
    print("[Desafio 1] Finalizado.\n")

# -------------------------- Desafio 2 --------------------------
def desafio2_fft_e_stft():
    """
    2) Análise espectral tradicional + chirp + espectrograma (STFT)
    """
    print("\n[Desafio 2] FFT + Chirp + Espectrograma (STFT)")
    # Chirp linear (150 -> 450 Hz)
    Fs = 10000
    t1 = 3.0     # queremos 3 segundos (no Colab ficou 0.2 s por engano)
    f0 = 150
    f1 = 450
    k  = (f1 - f0) / t1

    t = np.arange(0, t1, 1/Fs)
    y = np.cos(2*np.pi*(f0*t + 0.5*k*t**2))

    print(f"Duração do áudio: {seconds_str(len(y), Fs)}")
    # FFT para ver “conteúdo global”
    Y = np.abs(fft(y))
    freq = fftfreq(len(y), 1/Fs)[:len(y)//2]

    plt.figure(figsize=(10,3))
    plt.plot(t, y)
    plt.title("Chirp linear (150->450 Hz)")
    plt.xlabel("Tempo (s)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10,3))
    plt.plot(freq, Y[:len(freq)])
    plt.title("Espectro de Magnitude (FFT)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("|Y|")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("Reproduzindo o chirp (3 s)...")
    play_audio(y, Fs)

    # Espectrograma (tempo x frequência)
    f, tt, Sxx = signal.spectrogram(y, Fs, nperseg=1024, noverlap=512, nfft=2048)
    plt.figure(figsize=(10,4))
    plt.pcolormesh(tt, f, Sxx, shading="gouraud")
    plt.ylabel("Frequência (Hz)")
    plt.xlabel("Tempo (s)")
    plt.title("Espectrograma (STFT)")
    plt.colorbar(label="Energia")
    plt.tight_layout()
    plt.show()

    print("[Desafio 2] Finalizado.\n")

# -------------------------- Desafio 3 --------------------------
def desafio3_esteganografia():
    """
    3) “Ouvir imagens?”: carrega lena.wav e faz espectrogramas,
       incluindo variação de parâmetros; opcional: baleias (whalecalls.mat)
    """
    print("\n[Desafio 3] Esteganografia / Ouvir imagens?")
    # --- Parte 1: lena.wav ---
    lena_url = "https://raw.githubusercontent.com/nias-ufv/elt576-processamento-inteligente-sinais/main/semana-3/lena.wav"
    lena_path = os.path.join(DATA, "lena.wav")
    download_if_missing(lena_url, lena_path)

    try:
        samplerate, lena = wavfile.read(lena_path)
        print(f"lena.wav -> Fs={samplerate} Hz | {seconds_str(len(lena), samplerate)}")
        # normalizar se for int
        if lena.dtype != np.float32:
            lena = lena.astype(np.float32) / (np.max(np.abs(lena)) or 1.0)
        print("Reproduzindo lena.wav ...")
        play_audio(lena, samplerate)

        # espectrograma padrão
        f1, t1, Sxx1 = signal.spectrogram(lena, samplerate)
        plt.figure(figsize=(10,4))
        plt.pcolormesh(t1, f1, Sxx1, shading="gouraud", cmap="gray")
        plt.ylabel("Frequência (Hz)")
        plt.xlabel("Tempo (s)")
        plt.ylim(0, samplerate/2)
        plt.title("Espectrograma (padrão)")
        plt.tight_layout()
        plt.show()

        # variar nperseg
        npersegs = [256, 1024, 4096, 8192]
        fig, ax = plt.subplots(1, len(npersegs), sharey=True, figsize=(16,4))
        for i, nperseg in enumerate(npersegs):
            f2, t2, Sxx2 = signal.spectrogram(lena, samplerate, nperseg=nperseg)
            ax[i].pcolormesh(t2, f2, Sxx2, shading="gouraud", cmap="gray")
            ax[i].set_title(f"nperseg={nperseg}")
            ax[i].set_xlabel("Tempo (s)")
        ax[0].set_ylabel("Frequência (Hz)")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[Aviso] Não foi possível processar lena.wav: {e}")

    # --- Parte 2 (opcional): baleias ---
    print("\n[Opcional] Canto das baleias (whalecalls.mat)")
    whales_url = "https://raw.githubusercontent.com/nias-ufv/elt576-processamento-inteligente-sinais/main/semana-3/whalecalls.mat"
    whales_path = os.path.join(DATA, "whalecalls.mat")
    download_if_missing(whales_url, whales_path)

    if os.path.exists(whales_path):
        try:
            whales = loadmat(whales_path)
            fs = float(whales["fs"][0][0])
            X1 = whales["X1"]
            X2 = whales["X2"]
            print(f"whalecalls.mat -> fs={fs} Hz | X1 shape={X1.shape} | X2 shape={X2.shape}")

            # tocar um exemplo
            if X1.shape[0] > 0:
                print("Reproduzindo um chamado de X1 ...")
                play_audio(X1[0].astype(np.float32) / (np.max(np.abs(X1[0])) or 1.0), int(fs))

            # espectrogramas de algumas faixas de X1
            n_show = min(6, X1.shape[0])
            fig, ax = plt.subplots(2, math.ceil(n_show/2), sharey=True, figsize=(14,6))
            ax = ax.ravel()
            for i in range(n_show):
                fX, tX, SxxX = signal.spectrogram(X1[i], fs)
                ax[i].pcolormesh(tX, fX, SxxX, shading="gouraud", cmap="gray")
                ax[i].set_title(f"X1 faixa {i+1}")
                ax[i].set_xlabel("Tempo (s)")
            ax[0].set_ylabel("Frequência (Hz)")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"[Aviso] Não foi possível processar whalecalls.mat: {e}")
    else:
        print("Coloque whalecalls.mat em ./data para explorar os espectrogramas.")

    print("[Desafio 3] Finalizado.\n")

# -------------------------- Menu --------------------------
def main():
    MENU = """
ELT 576 - Semana 3 - 123103 - Elmer Antonio Moreira Rodrigues
[1] Tempo <-> Frequência (FFT + IRFFT)          (Desafio 1)
[2] FFT + Chirp + Espectrograma (STFT)          (Desafio 2)
[3] Esteganografia / Ouvir imagens? + Baleias   (Desafio 3)
[0] Sair
Escolha: """
    while True:
        try:
            opt = input(MENU).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo...")
            break

        if opt == "1":
            desafio1_tempo_freq()
        elif opt == "2":
            desafio2_fft_e_stft()
        elif opt == "3":
            desafio3_esteganografia()
        elif opt == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
