# ELT574 - Aprendizado de Maquina (Machine Learning)

## Visao Geral

Disciplina focada nos fundamentos de aprendizado de maquina, abordando desde o perceptron simples ate redes neurais multicamadas, alem de tecnicas de analise e engenharia de features.

## Conteudos Aplicados

### 1. Perceptron Simples
- **Arquivo**: `ELT574-Perceptron.py`
- Implementacao do classificador Perceptron usando scikit-learn
- Treinamento no dataset Iris (classificacao binaria de 2 classes)
- Visualizacao de fronteiras de decisao com matplotlib
- Conceitos: pesos, bias, convergencia do perceptron

### 2. Perceptron Multicamadas / Redes Neurais Profundas
- **Arquivo**: `ELT574-Perceptron-Multicamadas.py`
- Uso do TensorFlow/Keras para construcao de redes neurais
- Treinamento no dataset Fashion MNIST
- Introducao ao deep learning com multiplas camadas ocultas

### 3. Analise de Dados e Correlacao
- **Arquivo**: `ELT574-123103-Atividade-1.py`
- Carregamento e exploracao do dataset de precos de imoveis (Melbourne)
- Analise de correlacao entre features e variavel alvo
- Engenharia de features (calculo de total de comodos)
- Interpretacao de coeficientes de correlacao

### 4. Atividades Praticas
- **Arquivo**: `ELT574-123103-Atividade-2.py` - Classificacao com Perceptron
- **Arquivo**: `ELT574-123103-Atividade-3.py` - Visualizacao de fronteiras de decisao

## Datasets Utilizados

| Dataset | Arquivo | Descricao |
|---------|---------|-----------|
| Iris | `data/iris.data` | Classificacao de especies de flores |
| Melbourne Housing | `data/melb_data.csv` | Precos de imoveis em Melbourne |
| California Housing | `data/housing.csv` | Precos de imoveis na California |
| Spotify | `data/musicas_spotify_limpo.csv` | Features de musicas do Spotify |

## Bibliotecas Utilizadas

- **scikit-learn**: Perceptron, metricas de avaliacao
- **TensorFlow/Keras**: Redes neurais multicamadas
- **NumPy**: Manipulacao de arrays e operacoes numericas
- **Pandas**: Analise e manipulacao de dados tabulares
- **Matplotlib**: Visualizacao de graficos e fronteiras de decisao

## Conceitos-Chave

- Aprendizado supervisionado (classificacao)
- Perceptron e regra de aprendizado
- Redes neurais artificiais (MLP)
- Fronteiras de decisao
- Engenharia e selecao de features
- Analise de correlacao
