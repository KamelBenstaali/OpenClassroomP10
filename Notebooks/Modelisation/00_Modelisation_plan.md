# Plan d'Exécution de la Modélisation

## 1. Contexte et Synthèse du Projet
- Définition du contexte de la mission (Start-up My Content).
- Identification de la fonctionnalité critique (recommandation de 5 articles).
- L'objectif est de benchmarker (comparer) différentes approches pour trouver le meilleur modèle MVP à déployer sur Azure Functions (Serverless).

## 2. Structure des Notebooks d'Expérimentation
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

---
*(Note : Le fichier `04_modelisation.ipynb` contenait de premières ébauches exploratoires et n'est plus utilisé activement dans ce pipeline de benchmark structuré).*
