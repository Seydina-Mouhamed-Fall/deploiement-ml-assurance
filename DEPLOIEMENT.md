# Déploiement du modèle de prédiction des dépenses (expenses)

## Étapes chronologiques pour lancer le serveur localement

### 1. Se placer dans le dossier du projet

```powershell
cd "c:\Users\medme\Desktop\Machine Learning\ML_EXAM"
```

### 2. Créer et activer un environnement virtuel (recommandé)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```powershell
pip install -r requirements.txt
```

### 4. Exporter le modèle (créer model.pkl et columns.json)

```powershell
python export_model.py
```

> Si `best_model.joblib` existe (après exécution du notebook), il sera chargé et exporté en .pkl.  
> Sinon, le script entraîne un Random Forest sur insurance.csv et crée model.pkl.

### 5. Lancer le serveur Flask

```powershell
python app.py
```

### 6. Ouvrir l’application

Ouvrir un navigateur et aller sur :  
**http://127.0.0.1:5000**

---

## Structure des fichiers

```
ML_EXAM/
├── app.py              # Application Flask
├── export_model.py     # Export du modèle (.pkl) et colonnes (columns.json)
├── model.pkl           # Modèle Random Forest (créé par export_model.py)
├── columns.json        # Ordre des features (créé par export_model.py)
├── insurance.csv       # Jeu de données (ou Insurance.csv)
├── best_model.joblib   # Optionnel : modèle du notebook ML.ipynb
├── requirements.txt    # Dépendances Python
├── templates/
│   └── index.html      # Interface web du formulaire
└── DEPLOIEMENT.md      # Ce fichier
```

## Champs du formulaire

| Champ   | Type   | Exemple                                    |
| ------- | ------ | ------------------------------------------ |
| Âge     | number | 18–64                                      |
| Sexe    | select | male / female                              |
| IMC     | number | 15–55 (ex: 28.5)                           |
| Enfants | number | 0–5                                        |
| Fumeur  | select | yes / no                                   |
| Région  | select | northeast, northwest, southeast, southwest |

## Résultat

La prédiction s’affiche en USD (ex : **$12 345.67**).

---

                                            RERUN

Procédure de redémarrage

1. Naviguer vers le bon dossier
   Assure-toi que ton terminal pointe sur le répertoire exact contenant ton fichier app.py. S'il se trouve dans le sous-dossier de ton projet, déplace-toi :

PowerShell

cd "C:\Users\medme\Desktop\Machine Learning\ML_EXAM\deploy_model_regression" 2. Activer l'environnement virtuel (Étape critique)
Rattache ton terminal à l'environnement isolé que tu as créé.

PowerShell

.\venv\Scripts\activate
Vérification : Tu dois impérativement voir (venv) apparaître au début de ta ligne de commande.

3. Lancer le serveur d'application
   Exécute le script principal pour démarrer le moteur Flask.

PowerShell

python app.py 4. Accéder à l'interface utilisateur
Le terminal va se bloquer et afficher une adresse d'écoute. Ouvre ton navigateur web (Chrome, Edge, etc.) et rends-toi à cette adresse locale :

http://127.0.0.1:5000
