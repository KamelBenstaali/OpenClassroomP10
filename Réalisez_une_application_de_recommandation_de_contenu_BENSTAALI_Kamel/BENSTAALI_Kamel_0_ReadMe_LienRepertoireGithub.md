# Projet P10 - GloboNews : Système de Recommandation Hybride

Lien Github Repo: 
https://github.com/KamelBenstaali/OpenClassroomP10


Bienvenue dans le dépôt du projet GloboNews (Start-up My Content). L'objectif de ce projet est de développer un MVP (Minimum Viable Product) d'une application de recommandation d'articles utilisant une intelligence artificielle hybride et une architecture cloud serverless (Azure Functions).

## Architecture Globale

Le projet se décompose en 3 grandes briques :
1. **Machine Learning (Notebooks) :** Benchmark, modélisation et création de l'algorithme Hybride (ALS + Content-Based + Time Decay).
2. **Backend Serverless (AzureAPI) :** Une API REST Python déployée sur Azure Functions qui charge les modèles pré-entraînés et calcule les recommandations en temps réel.
3. **Frontend (Streamlit) :** Une application web interactive simulant l'expérience utilisateur finale.

## Jeu de Données (Dataset)

Le projet exploite le jeu de données public **"News Portal User Interactions by Globo.com"**. Ce dataset représente des interactions réelles de lecteurs avec des articles de presse. Il fournit deux sources d'informations cruciales :
- **Les interactions (Clics) :** Un historique massif des sessions utilisateurs, incluant l'ID de l'utilisateur, l'ID de l'article lu, et le timestamp (heure du clic).
- **Les métadonnées des articles :** Des informations sur chaque article (catégorie, nombre de mots) ainsi que des "Word Embeddings" (plongements lexicaux) pré-calculés, qui ont servi de base à notre algorithme Content-Based.

## Structure du Dépôt

Le projet est organisé selon l'arborescence suivante :

- **`Data/`** : Ce dossier contient les jeux de données bruts et traités nécessaires au projet (historique de clics, informations sur les articles, embeddings pré-calculés, etc.).
- **`Generated/`** : Dossier utilisé pour stocker les fichiers ou les modèles générés automatiquement lors des différentes étapes d'entraînement (matrices ALS, objets PCA, dictionnaires).
- **`AzureAPI/`** : Code source de l'API Serverless (Azure Functions). Contient le fichier `function_app.py` et le dossier `data/` abritant les matrices du modèle (Numpy/Pickle).
- **`Frontend/`** : Code source de l'interface utilisateur web développée avec `streamlit_app.py`.
- **`.github/workflows/`** : Pipeline CI/CD (GitHub Actions) pour le déploiement continu automatisé vers Microsoft Azure.
- **`Notebooks/Modelisation/`** : Contient tous les notebooks Jupyter d'entraînement et d'évaluation (Collaboratif, Content-Based, et Hybride).
- **`Guides/`** : Documentation et tutoriels techniques pour le déploiement et la gestion d'Azure Functions.
- **`Détails_mission/`** : Documentation concernant les spécifications initiales et le périmètre du projet.

*(Note : Les environnements virtuels `.venv` sont exclus de Git via le `.gitignore`).*

## Plan d'Exécution de la Modélisation (Dossier `Notebooks/Modelisation/`)

L'exploration algorithmique a été découpée en plusieurs notebooks spécialisés afin de garder un code propre, modulaire et d'isoler les benchmarks de chaque famille d'algorithmes :

### 📓 `01_Collaborative_models.ipynb`
Ce notebook est dédié à la recommandation par filtrage collaboratif (analyse de la matrice d'interactions Utilisateurs-Articles).
**Travail réalisé :**
- Création d'une matrice creuse (sparse matrix) optimisée en mémoire.
- Entraînement et évaluation du modèle **SVD** (Surprise) avec adaptation des clics en notes (ratings).
- Entraînement et évaluation du modèle **ALS** (Alternating Least Squares de la librairie `implicit`), spécialement conçu pour les données de feedback implicite.
- **Résultat :** L'algorithme ALS s'est imposé grâce à ses excellentes performances de calcul (matrices creuses) et son Hit Ratio très satisfaisant.

### 📓 `02_Content_based_models.ipynb`
Ce notebook explore la recommandation par le contenu, en se basant sur les caractéristiques vectorielles des articles.
**Travail réalisé :**
- Importation des plongements de mots (Word Embeddings) pré-entraînés fournis dans le dataset (`articles_embeddings.pickle`).
- Réduction de dimension avec **PCA (Analyse en Composantes Principales)** pour réduire la taille des vecteurs de 250 à 50 dimensions (préservant plus de 85% de la variance).
- Calcul de la **Similarité Cosinus** pour trouver mathématiquement les articles les plus proches sémantiquement du dernier article lu par l'utilisateur.

### 📓 `03_Hybrid_models.ipynb`
Ce notebook est l'étape de synthèse : il fusionne les modèles précédents pour créer le "Cerveau" final de l'application et régler le problème majeur des nouveaux utilisateurs.
**Travail réalisé :**
- **Algorithme de Popularité (Time Decay) :** Création d'un système de secours (Fallback) pour le Cold-Start. Les articles les plus cliqués voient leur score baisser au fil des jours (Time Decay) pour éviter de toujours recommander de vieux articles.
- **Le Modèle Hybride :** Création de la fonction maîtresse qui appelle ALS (poids: 0.74), le Content-Based (poids: 0.19), et la Popularité (poids: 0.15). Les scores sont normalisés (MinMaxScaler) et combinés.
- **Exportation pour la Production :** Sauvegarde des matrices facteurs ALS (`.npy`), des dictionnaires de mapping (`.pkl`), et des données PCA (`.pickle`) dans le dossier `Generated/` pour être ingérés par l'API Serverless Azure.

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

*(Aperçu de l'interface utilisateur Streamlit)*
![Interface Streamlit GloboNews](Support_presentation/UI.png)

## Déploiement et CI/CD

Ce projet intègre Git LFS pour le stockage des artefacts de Machine Learning.
Le pipeline CI/CD configuré via GitHub Actions permet de compiler et déployer automatiquement l'API sur Microsoft Azure à chaque "push" sur la branche `main`.