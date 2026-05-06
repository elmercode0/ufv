# ELT579 - Aprendizado de Maquina Aplicado (Competicoes e Aplicacoes Reais)

## Visao Geral

Disciplina com foco pratico em aprendizado de maquina, utilizando competicoes estilo Kaggle e problemas do mundo real. Aborda pipeline completo de ML: preprocessamento, engenharia de features, treinamento de multiplos modelos, otimizacao de hiperparametros e avaliacao.

## Conteudos Aplicados

### Aula 1 - Classificacao: Predicao de Sobrevivencia no Titanic

#### Pipeline Completo de Classificacao
- **Arquivos**: `aula1/titanic.py`, `aula1/titanic_refactored.py`, `aula1/elt579_titanic_teste_123103.ipynb`
- **Dataset**: Competicao Titanic do Kaggle

**Engenharia de Features aplicada**:
- Codificacao de genero (Sex -> numerico)
- Tratamento de valores ausentes (Fare, Age)
- Mapeamento de porto de embarque (Embarked)
- Criacao de feature "Child" (deteccao de criancas)

**Modelos de Classificacao implementados**:
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)
- Gaussian Naive Bayes
- Decision Trees
- Random Forest
- Voting Classifier (ensemble por votacao)

**Tecnicas de Avaliacao e Otimizacao**:
- GridSearchCV para busca de hiperparametros
- Stratified K-Fold Cross-Validation
- Matrizes de confusao
- Comparacao de desempenho entre modelos

### Aula 2 - Regressao e Selecao de Features

#### Selecao Otima de Features
- **Arquivos**: `aula2/script_problema2.py`, `aula2/elt579-aula2-123103.ipynb`
- **Dataset**: Severidade de doencas em tomate

**Tecnicas aplicadas**:
- Divisao treino-teste (80-20)
- Normalizacao com StandardScaler
- Recursive Feature Elimination (RFE) com LinearRegression
- Validacao cruzada para scoring
- Selecao do numero otimo de features (testando de 1 a 20)

## Datasets Utilizados

| Dataset | Arquivo | Descricao |
|---------|---------|-----------|
| Titanic Train | `data/train.csv` | Dados de treino da competicao Titanic |
| Titanic Test | `data/test.csv` | Dados de teste da competicao Titanic |
| Gender Submission | `data/gender_submission.csv` | Baseline de submissao |
| Tomato Disease | `aula2/dataset_problema2.csv` | Severidade de doencas em tomate |

**Submissoes geradas**:
- `123103_submission_knn.csv` - Predicoes com KNN
- `123103_submission_lr.csv` - Predicoes com Logistic Regression
- `123103_submission_lr_sc.csv` - Predicoes com LR + StandardScaler
- `123103_submission_model_forest.csv` - Predicoes com Random Forest
- `123103_submission_model_svm.csv` - Predicoes com SVM

## Bibliotecas Utilizadas

- **scikit-learn**: Modelos (LogisticRegression, KNN, SVM, DecisionTree, RandomForest, GaussianNB, VotingClassifier), preprocessamento (StandardScaler, LabelEncoder), selecao de features (RFE), validacao (GridSearchCV, cross_val_score, StratifiedKFold)
- **Pandas**: Manipulacao de DataFrames, limpeza de dados
- **NumPy**: Operacoes numericas
- **Matplotlib/Seaborn**: Visualizacao de resultados e matrizes de confusao

## Conceitos-Chave

- Pipeline completo de Machine Learning
- Engenharia de features para dados tabulares
- Comparacao sistematica de classificadores
- Metodos ensemble (Voting Classifier)
- Otimizacao de hiperparametros (Grid Search)
- Validacao cruzada estratificada
- Selecao de features (RFE)
- Regressao linear
- Normalizacao de dados
- Competicoes de ML (formato Kaggle)
