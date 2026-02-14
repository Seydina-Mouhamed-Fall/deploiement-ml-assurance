"""
Script d'export : charge le modèle .joblib (si existant) ou entraîne un Random Forest
sur Insurance.csv, puis sauvegarde model.pkl et columns.json.
"""
import pandas as pd
import joblib
import json
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_JOBLIB = os.path.join(BASE_DIR, 'best_model.joblib')
MODEL_PKL = os.path.join(BASE_DIR, 'model.pkl')
COLUMNS_JSON = os.path.join(BASE_DIR, 'columns.json')
DATA_CSV = os.path.join(BASE_DIR, 'insurance.csv')
DATA_CSV_ALT = os.path.join(BASE_DIR, 'Insurance.csv')

def train_model():
    """Entraîne Random Forest régularisé sur Insurance.csv."""
    path = DATA_CSV if os.path.exists(DATA_CSV) else DATA_CSV_ALT
    if not path or not os.path.exists(path):
        raise FileNotFoundError("insurance.csv ou Insurance.csv introuvable.")
    df = pd.read_csv(path)
    if 'charges' in df.columns and 'expenses' not in df.columns:
        df = df.rename(columns={'charges': 'expenses'})
    X = df.drop(columns=['expenses'])
    y = df['expenses']
    X_enc = pd.get_dummies(X, columns=['sex', 'smoker', 'region'])
    X_train, X_test, y_train, y_test = train_test_split(X_enc, y, test_size=0.3, random_state=42)
    model = RandomForestRegressor(
        n_estimators=100, max_depth=12, min_samples_leaf=5,
        min_samples_split=10, random_state=42
    )
    model.fit(X_train, y_train)
    r2 = model.score(X_test, y_test)
    print(f"R² test : {r2:.4f}")
    return model, X_enc.columns.tolist()

# 1. Charger ou entraîner le modèle
if os.path.exists(MODEL_JOBLIB):
    model = joblib.load(MODEL_JOBLIB)
    print(f"Modèle chargé depuis {MODEL_JOBLIB}")
    path = DATA_CSV if os.path.exists(DATA_CSV) else DATA_CSV_ALT
    if path and os.path.exists(path):
        df = pd.read_csv(path)
        if 'charges' in df.columns and 'expenses' not in df.columns:
            df = df.rename(columns={'charges': 'expenses'})
        X = df.drop(columns=['expenses'])
        X_enc = pd.get_dummies(X, columns=['sex', 'smoker', 'region'])
        columns = X_enc.columns.tolist()
    else:
        columns = ['age', 'bmi', 'children', 'sex_female', 'sex_male',
                   'smoker_no', 'smoker_yes', 'region_northeast',
                   'region_northwest', 'region_southeast', 'region_southwest']
else:
    print("best_model.joblib introuvable. Entraînement du Random Forest...")
    model, columns = train_model()

joblib.dump(model, MODEL_PKL)
print(f"Modèle exporté : {MODEL_PKL}")

# 2. Sauvegarder columns.json
with open(COLUMNS_JSON, 'w', encoding='utf-8') as f:
    json.dump(columns, f, indent=2)
print(f"Colonnes exportées : {COLUMNS_JSON}")
