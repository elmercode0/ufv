# titanic_refactored.py
# Refatorado para maior acurácia com engenharia de atributos + HistGradientBoosting
# Uso:
#   python titanic_refactored.py
# Requisitos:
#   pip install pandas numpy scikit-learn

import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingClassifier
import os


# -----------------------------
# Utils: extração de título do nome
# -----------------------------
def extract_title(name: str) -> str:
    title = name.split(",")[1].split(".")[0].strip()
    mapping = {
        "Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs",
        "Lady": "Rare", "Countess": "Rare", "Capt": "Rare", "Col": "Rare",
        "Don": "Rare", "Dr": "Rare", "Major": "Rare", "Rev": "Rare",
        "Sir": "Rare", "Jonkheer": "Rare", "Dona": "Rare"
    }
    return mapping.get(title, title)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Categorias básicas
    out["Sex"] = out["Sex"].astype("category")
    out["Embarked"] = out["Embarked"].fillna("S").astype("category")

    # Título
    out["Title"] = out["Name"].apply(extract_title)
    rare_titles = out["Title"].value_counts()[out["Title"].value_counts() < 10].index
    out["Title"] = out["Title"].apply(lambda x: "Rare" if x in rare_titles else x).astype("category")

    # Tamanho da família e indicadores
    out["FamilySize"] = out["SibSp"] + out["Parch"] + 1
    out["IsAlone"] = (out["FamilySize"] == 1).astype(int)

    # Tamanho do grupo por ticket
    out["TicketGroupSize"] = out.groupby("Ticket")["Ticket"].transform("count")

    # Deck da cabine + tem cabine?
    out["CabinDeck"] = out["Cabin"].astype(str).str[0].replace({"n": "U"}).astype("category")
    out["HasCabin"] = (~out["Cabin"].isna()).astype(int)

    # Interações úteis
    out["Pclass*Sex"] = out["Pclass"].astype(str) + "_" + out["Sex"].astype(str)
    out["Pclass*Title"] = out["Pclass"].astype(str) + "_" + out["Title"].astype(str)
    out["Pclass*Sex"] = out["Pclass*Sex"].astype("category")
    out["Pclass*Title"] = out["Pclass*Title"].astype("category")

    return out

def get_next_filename(base_name: str) -> str:
    if not os.path.exists(base_name):
        return base_name

    base, ext = os.path.splitext(base_name)
    i = 2
    new_name = f"{base}_{i}{ext}"
    while os.path.exists(new_name):
        i += 1
        new_name = f"{base}_{i}{ext}"
    return new_name

def main(train_path="data/train.csv", test_path="data/test.csv", out_path="submission_titanic_refactor.csv"):
    # -----------------------------
    # Carregar dados
    # -----------------------------
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    # Concatenar para engenharia de atributos consistente
    full = pd.concat([train.drop(columns=["Survived"]), test], axis=0, ignore_index=True)
    full = add_engineered_features(full)

    # Imputação de Fare por mediana dentro de Pclass
    fare_median_by_pclass = full.groupby("Pclass")["Fare"].median()
    full["Fare"] = full.apply(
        lambda r: fare_median_by_pclass[r["Pclass"]] if pd.isna(r["Fare"]) else r["Fare"],
        axis=1
    )

    # Idade por mediana do grupo (Title, Pclass, Sex)
    age_group_median = full.groupby(["Title", "Pclass", "Sex"])["Age"].median()
    full["Age"] = full.apply(
        lambda r: age_group_median.get((r["Title"], r["Pclass"], r["Sex"]), full["Age"].median())
        if pd.isna(r["Age"]) else r["Age"],
        axis=1
    )

    # Atributos derivados de custo por pessoa/grupo
    full["FarePerTicketGroup"] = full["Fare"] / full["TicketGroupSize"].replace(0, 1)
    full["FarePerPerson"] = full["Fare"] / full["FamilySize"].replace(0, 1)

    # -----------------------------
    # Seleção de features
    # -----------------------------
    num_features = [
        "Age", "SibSp", "Parch", "Fare",
        "FamilySize", "IsAlone", "TicketGroupSize",
        "FarePerTicketGroup", "FarePerPerson",
    ]

    cat_features = [
        "Pclass", "Sex", "Embarked", "Title",
        "CabinDeck", "Pclass*Sex", "Pclass*Title", "HasCabin",
    ]

    X_all = full[num_features + cat_features].copy()
    X_train = X_all.iloc[: len(train), :].copy()
    X_test = X_all.iloc[len(train) :, :].copy()
    y_train = train["Survived"].astype(int).values

    # -----------------------------
    # Pré-processamento
    # -----------------------------
    numeric_transformer = SimpleImputer(strategy="median")
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            # use 'sparse=False' para compatibilidade com versões antigas do sklearn
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocess = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_features),
            ("cat", categorical_transformer, cat_features),
        ]
    )

    # -----------------------------
    # Modelo (boosting tabular)
    # -----------------------------
    model = Pipeline(
        steps=[
            ("prep", preprocess),
            ("clf", HistGradientBoostingClassifier(
                max_leaf_nodes=31,
                learning_rate=0.06,
                min_samples_leaf=20,
                random_state=42,
            )),
        ]
    )

    # -----------------------------
    # Validação cruzada (rápida)
    # -----------------------------
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy", n_jobs=-1)
    print(f"CV accuracy (5-fold): {scores.mean():.4f} ± {scores.std():.4f}")

    # -----------------------------
    # Treinar no conjunto completo e exportar submissão
    # -----------------------------
    model.fit(X_train, y_train)
    test_pred = model.predict(X_test).astype(int)

    submission = pd.DataFrame({
        "PassengerId": test["PassengerId"],
        "Survived": test_pred
    })
    submission.to_csv(get_next_filename(out_path), index=False)
    print(f"Arquivo de submissão salvo em: {Path(out_path).resolve()}")


if __name__ == "__main__":
    main()
