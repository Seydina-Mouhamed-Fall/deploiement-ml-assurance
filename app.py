"""
Application Flask - Prédiction des dépenses médicales (expenses)
Modèle : Random Forest entraîné sur Insurance.csv
"""
import os
import json
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
COLUMNS_PATH = os.path.join(BASE_DIR, 'columns.json')

# Charger le modèle et les colonnes au démarrage
model = None
FEATURE_COLUMNS = []

def load_model():
    global model, FEATURE_COLUMNS
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    if os.path.exists(COLUMNS_PATH):
        with open(COLUMNS_PATH, 'r', encoding='utf-8') as f:
            FEATURE_COLUMNS = json.load(f)

load_model()

def preprocess_input(age, sex, bmi, children, smoker, region):
    """Encode les variables catégorielles et aligne avec les colonnes du modèle."""
    df = pd.DataFrame([{
        'age': int(age),
        'bmi': float(bmi),
        'children': int(children),
        'sex': sex.lower(),
        'smoker': smoker.lower(),
        'region': region.lower()
    }])
    df_enc = pd.get_dummies(df, columns=['sex', 'smoker', 'region'])
    # Aligner les colonnes
    for col in FEATURE_COLUMNS:
        if col not in df_enc.columns:
            df_enc[col] = 0
    df_enc = df_enc[FEATURE_COLUMNS]
    return df_enc

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Modèle non chargé. Exécutez export_model.py d\'abord.'}), 500
    
    try:
        data = request.get_json() or request.form
        age = int(data.get('age', 0))
        sex = data.get('sex', 'male')
        bmi = float(data.get('bmi', 0))
        children = int(data.get('children', 0))
        smoker = data.get('smoker', 'no')
        region = data.get('region', 'southwest')
        
        X = preprocess_input(age, sex, bmi, children, smoker, region)
        prediction = model.predict(X)[0]
        
        return jsonify({
            'success': True,
            'prediction': round(float(prediction), 2),
            'expenses': round(float(prediction), 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    if model is None:
        print("ATTENTION: Exécutez 'python export_model.py' avant de lancer l'app.")
    app.run(debug=True, host='0.0.0.0', port=5000)
