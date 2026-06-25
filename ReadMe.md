# Projet P10 - GloboNews : Système de Recommandation Hybride

Bienvenue dans le dépôt du projet GloboNews (Start-up My Content). L'objectif de ce projet est de développer un MVP (Minimum Viable Product) d'une application de recommandation d'articles utilisant une intelligence artificielle hybride et une architecture cloud serverless (Azure Functions).

## Architecture Globale

Le projet se décompose en 3 grandes briques :
1. **Machine Learning (Notebooks) :** Benchmark, modélisation et création de l'algorithme Hybride (ALS + Content-Based + Time Decay).
2. **Backend Serverless (AzureAPI) :** Une API REST Python déployée sur Azure Functions qui charge les modèles pré-entraînés et calcule les recommandations en temps réel.
3. **Frontend (Streamlit) :** Une application web interactive simulant l'expérience utilisateur finale.

## Structure du Dépôt

Le projet est organisé selon l'arborescence suivante :

- **`AzureAPI/`** : Code source de l'API Serverless (Azure Functions). Contient le fichier `function_app.py` et le dossier `data/` abritant les matrices du modèle (Numpy/Pickle).
- **`Frontend/`** : Code source de l'interface utilisateur web développée avec `streamlit_app.py`.
- **`.github/workflows/`** : Pipeline CI/CD (GitHub Actions) pour le déploiement continu automatisé vers Microsoft Azure.
- **`Notebooks/Modelisation/`** : Contient tous les notebooks Jupyter d'entraînement et d'évaluation (Collaboratif, Content-Based, et Hybride).
- **`Guides/`** : Documentation et tutoriels techniques pour le déploiement et la gestion d'Azure Functions.
- **`Détails_mission/`** : Documentation concernant les spécifications initiales et le périmètre du projet.

*(Note : Les dossiers `Data/` et `Generated/` contenant les datasets lourds bruts sont exclus de Git via le `.gitignore`, tout comme les environnements virtuels `.venv`).*

## Lancement en Local

### 1. Démarrer l'API (Backend)
```bash
cd AzureAPI
func start
```
L'API écoutera sur `http://localhost:7071/api/recommend`.

### 2. Démarrer l'Interface (Frontend)
Dans un nouveau terminal :
```bash
cd Frontend
streamlit run streamlit_app.py
```
L'application web s'ouvrira sur `http://localhost:8501`.

## Déploiement et CI/CD

Ce projet intègre Git LFS pour le stockage des artefacts de Machine Learning.
Le pipeline CI/CD configuré via GitHub Actions permet de compiler et déployer automatiquement l'API sur Microsoft Azure à chaque "push" sur la branche `main`.