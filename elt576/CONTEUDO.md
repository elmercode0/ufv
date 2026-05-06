# ELT576 - Processamento de Sinais

## Visao Geral

Disciplina focada em processamento digital de sinais, abrangendo convolucao (1D e 2D), transformada de Fourier, analise espectral, processamento de audio e processamento de imagens.

## Conteudos Aplicados

### Atividade 1 - Convolucao e Filtragem

#### Desafio 1: Resposta ao Impulso e Convolucao 1D
- **Arquivo**: `elt576_atividade1_desafio1_123103.py`
- Criacao de respostas ao impulso h[n]
- Aplicacao de convolucao entre sinais usando `numpy.convolve()`
- Visualizacao de sinais no dominio do tempo

#### Desafio 2: Filtragem de Audio (Trompete)
- **Arquivo**: `elt576_atividade1_desafio2_123103.py`
- Carregamento de arquivo .mat com amostras de audio de trompete
- Aplicacao de filtros convolucionais em sinais de audio
- Comparacao visual entre sinal original e filtrado

#### Desafio 3: Processamento de Imagem com Filtro Laplaciano
- **Arquivo**: `elt576_atividade1_desafio3_123103.py`
- Carregamento de imagem da lua (`img/lua.jpg`)
- Convolucao 2D com kernel Laplaciano
- Realce de imagem por deteccao de bordas
- Visualizacao: imagem original, convoluida e realcada

#### Desafio 4: Filtragem 2D de Imagem
- **Arquivo**: `elt576_atividade1_desafio4_123103.py`
- Processamento de imagem de texto (`img/texto.jpg`)
- Aplicacao de kernel de convolucao 2D personalizado

### Atividade 2 - Transformada de Fourier e Analise Espectral

#### Desafio 1: FFT e Analise no Dominio da Frequencia
- **Arquivos**: `elt576_atividade2_desafio1.1_123103.py`, `elt576_atividade2_desafio1.2_123103.py`
- Geracao de sinais senoidais no dominio do tempo
- Calculo da FFT e visualizacao no dominio da frequencia
- FFT simetrica e apenas frequencias positivas
- Reconstrucao de sinal via FFT inversa (irfft)

#### Desafio 2: Espectrograma
- **Arquivo**: `elt576_atividade2_desafio2_123103.py`
- Geracao de sinais de varredura senoidal (chirp)
- Analise tempo-frequencia com `scipy.signal.spectrogram()`
- Reproducao de audio com biblioteca `sounddevice`
- Visualizacao de espectrogramas

#### Desafio 3: Processamento Avancado de Audio
- **Arquivo**: `elt576_atividade2_desafio3_123103.py`
- Analise FFT com tecnicas de janelamento
- Filtragem de ruido e reconstrucao de sinal

#### Desafio 4: Tecnicas Adicionais de Processamento
- **Arquivo**: `elt576_atividade2_desafio4_123103.py`
- Continuacao de tecnicas de processamento de audio

#### Laboratorio Completo de Processamento de Sinais
- **Arquivo**: `elt576_atividade2_123103.py`
- Conversoes tempo-frequencia (FFT/IRFFT)
- Filtragem com diversas respostas ao impulso
- Efeitos de audio (reverb, simulacao de eco)
- Filtragem de ruido
- Geracao de espectrogramas
- STFT (Short-Time Fourier Transform)

## Datasets e Recursos Utilizados

| Recurso | Arquivo | Descricao |
|---------|---------|-----------|
| Lena Audio | `data/lena.wav` | Sinal de audio para testes |
| Bird Chirp | `data/bird2fil.wav` | Audio de canto de passaro |
| Whale Calls | `data/whalecalls.mat` | Sinais acusticos de baleias |
| Trumpet | `data/trumpet.mat` | Amostra de audio de trompete |
| Ruido | `data/ruido.txt` | Dados de ruido |
| Lua | `img/lua.jpg` | Imagem da lua para filtragem 2D |
| Texto | `img/texto.jpg` | Imagem de texto para filtragem 2D |

## Bibliotecas Utilizadas

- **NumPy**: Operacoes numericas, convolucao, FFT
- **SciPy**: `signal` (espectrograma, filtragem), `fft`, `io.wavfile`
- **Matplotlib**: Visualizacao de sinais, espectrogramas e imagens
- **PIL (Pillow)**: Carregamento e manipulacao de imagens
- **sounddevice**: Reproducao de audio

## Conceitos-Chave

- Convolucao 1D e 2D
- Resposta ao impulso de sistemas
- Transformada de Fourier (DFT/FFT) e inversa (IFFT/IRFFT)
- Dominio do tempo vs. dominio da frequencia
- Espectrogramas e analise tempo-frequencia
- STFT (Short-Time Fourier Transform)
- Filtragem de sinais (passa-baixa, passa-alta)
- Processamento de imagem (deteccao de bordas, realce)
- Processamento de audio (filtragem de ruido, efeitos)
- Funcoes de janelamento
