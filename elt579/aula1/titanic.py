import os
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier


# Carregar dados
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

print(train.info())


# Preparar dados e features
def criar_features(df: pd.DataFrame) -> pd.DataFrame:
    X = df.copy()
    subs = {'female': 1, 'male': 0}
    X['mulher'] = X['Sex'].replace(subs)

    X['Fare'] = X['Fare'].fillna(X['Fare'].mean())
    X['Age'] = X['Age'].fillna(X['Age'].mean())
    X['Embarked'] = X['Embarked'].fillna('S')

    subs = {'S': 1, 'C': 2, 'Q': 3}
    X['porto'] = X['Embarked'].replace(subs)

    X['crianca'] = np.where(X['Age'] < 12, 1, 0)

    features = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'mulher', 'porto', 'crianca']
    return X[features]


X_train = criar_features(train.drop(['PassengerId', 'Survived'], axis=1))
X_test = criar_features(test.drop(['PassengerId'], axis=1))
y_train = train['Survived']


# Validação cruzada consistente
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


# Definir modelos com pipelines (evita vazamento ao escalar dentro do CV)
model_specs = {
    'LogReg': {
        'estimator': Pipeline([
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(random_state=0, max_iter=1000))
        ]),
        'param_grid': {
            'model__C': [0.01, 0.1, 1, 3, 10],
            'model__penalty': ['l2'],
            'model__solver': ['liblinear', 'lbfgs']
        }
    },
    'KNN': {
        'estimator': Pipeline([
            ('scaler', StandardScaler()),
            ('model', KNeighborsClassifier())
        ]),
        'param_grid': {
            'model__n_neighbors': [3, 5, 7, 9, 11],
            'model__p': [1, 2]
        }
    },
    'SVC': {
        'estimator': Pipeline([
            ('scaler', StandardScaler()),
            ('model', SVC(kernel='rbf'))
        ]),
        'param_grid': {
            'model__C': [0.1, 1, 3, 10],
            'model__gamma': [0.01, 0.1, 0.3, 1.0]
        }
    },
    'GaussianNB': {
        'estimator': Pipeline([
            ('model', GaussianNB())
        ]),
        'param_grid': {
            'model__var_smoothing': np.logspace(-11, -8, 4)
        }
    },
    'DecisionTree': {
        'estimator': Pipeline([
            ('model', DecisionTreeClassifier(random_state=0))
        ]),
        'param_grid': {
            'model__criterion': ['gini', 'entropy'],
            'model__max_depth': [3, 4, 5, 6, None],
            'model__min_samples_split': [2, 5, 10],
            'model__min_samples_leaf': [1, 2, 4]
        }
    },
    'RandomForest': {
        'estimator': Pipeline([
            ('model', RandomForestClassifier(random_state=0, n_jobs=-1))
        ]),
        'param_grid': {
            'model__n_estimators': [200, 400, 800],
            'model__criterion': ['gini', 'entropy'],
            'model__max_depth': [None, 5, 8, 12],
            'model__min_samples_split': [2, 5, 10],
            'model__min_samples_leaf': [1, 2, 4]
        }
    }
}


# Treinar e avaliar cada modelo com GridSearchCV
results = []
best_estimators = {}

for name, spec in model_specs.items():
    gs = GridSearchCV(
        estimator=spec['estimator'],
        param_grid=spec['param_grid'],
        cv=cv,
        scoring='accuracy',
        n_jobs=-1,
        refit=True,
        verbose=0
    )
    gs.fit(X_train, y_train)
    results.append({
        'model': name,
        'best_score': float(gs.best_score_),
        'best_params': gs.best_params_
    })
    best_estimators[name] = gs.best_estimator_


# Opcional: VotingClassifier com os 3 melhores
results_sorted = sorted(results, key=lambda r: r['best_score'], reverse=True)
top3 = results_sorted[:3]
voting_estimators = [(r['model'], best_estimators[r['model']]) for r in top3]

voting_clf = VotingClassifier(estimators=voting_estimators, voting='hard', n_jobs=None)
voting_cv_score = cross_val_score(voting_clf, X_train, y_train, cv=cv, scoring='accuracy', n_jobs=-1).mean()

results_sorted.append({
    'model': f"Voting({'+'.join([n for n, _ in voting_estimators])})",
    'best_score': float(voting_cv_score),
    'best_params': {f'{name}': best_estimators[name].get_params() for name, _ in voting_estimators}
})


# Selecionar melhor técnica
best_entry = max(results_sorted, key=lambda r: r['best_score'])
best_name = best_entry['model']

if best_name.startswith('Voting('):
    best_model = voting_clf
    best_model.fit(X_train, y_train)
else:
    best_model = best_estimators[best_name]


# Avaliar no treino (matriz de confusão) para referência
y_pred_train = best_model.predict(X_train)
mc = confusion_matrix(y_train, y_pred_train)
print('Melhor modelo:', best_name)
print('CV accuracy:', best_entry['best_score'])
print('Matriz de confusão (treino):')
print(mc)


# Gerar previsões para o teste e salvar
out_dir = Path('elt579') / 'outputs'
out_dir.mkdir(parents=True, exist_ok=True)

y_pred_test = best_model.predict(X_test)
submission = pd.DataFrame({'PassengerId': test['PassengerId'], 'Survived': y_pred_test})

score_tag = f"{best_entry['best_score']:.4f}".replace('.', '_')
sub_path = out_dir / f"submission_best-{best_name}_acc-{score_tag}.csv"
submission.to_csv(sub_path, index=False)


# Salvar ranking de modelos
leaderboard = pd.DataFrame(results_sorted)
leaderboard_path = out_dir / 'model_leaderboard.csv'
leaderboard.to_csv(leaderboard_path, index=False)

print(f"Leaderboard salvo em: {leaderboard_path}")
print(f"Submission salvo em: {sub_path}")

