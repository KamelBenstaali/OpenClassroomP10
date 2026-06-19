# Plan d'Exécution de la Modélisation

## 1. Contexte et Synthèse du Projet
- Définition du contexte de la mission (Start-up My Content).
- Identification de la fonctionnalité critique (recommandation de 5 articles).
- L'objectif est de benchmarker (comparer) différentes approches pour trouver le meilleur modèle MVP à déployer sur Azure Functions (Serverless).

## 2. Structure des Notebooks d'Expérimentation
L'exploration algorithmique a été découpée en plusieurs notebooks spécialisés afin de garder un code propre, modulaire et d'isoler les benchmarks de chaque famille d'algorithmes :

### 📓 `01_Collaboratives_models.ipynb`
Ce notebook est dédié à la comparaison des algorithmes de filtrage collaboratif (qui se basent uniquement sur la matrice d'interactions Utilisateurs-Articles).  
**Actions prévues :**
- Implémentation d'un modèle **Memory-Based (KNN Users)**.
- Implémentation du modèle **SVD** (en improvisant un score de rating via un preprocessing, par exemple en transformant le nombre de clics).
- Utilisation du modèle **ALS** (Alternating Least Squares) optimisé pour l'Implicit Feedback.
- Comparaison des performances de ces 3 techniques collaboratives.

### 📓 `02_Content_based_models.ipynb`
Ce notebook explore la recommandation par le contenu, en se basant sur les caractéristiques (embeddings) des articles.  
**Actions prévues :**
- Utilisation de la **Similarité Cosinus** sur les embeddings ACP des articles (`articles_embeddings.pickle`).
- Test de nouvelles distances, comme la distance **Euclidienne**, pour trouver les articles similaires.
- Comparaison des métriques de performance et de temps de calcul (latence) entre les différentes formules de distance.

### 📓 `03_Comparing_approachs.ipynb`
Ce notebook est l'étape de synthèse, d'évaluation globale et d'analyse métier.  
**Actions prévues :**
- **Recherche sur la popularité (Cold Start) :** Tester différentes formules de popularité (ex: diviser le score par le nombre d'utilisateurs uniques ou amortir le score par l'âge/ancienneté de l'article).
- **Benchmark Final (Train/Test) :** Rejouer le test d'évaluation avec toutes les approches gagnantes, mais sur **tous** les utilisateurs (au lieu de 100).
- **Nouvelles métriques :** Intégration de nouvelles métriques (Hit Ratio@5, MRR, Couverture du catalogue) ainsi que les métriques techniques cruciales (Latence d'inférence, Taille de la matrice/modèle en mémoire).
- **Segmentation des utilisateurs :** Séparer les cas d'utilisation. Calculer et afficher graphiquement les performances de chaque modèle selon le profil de l'utilisateur (ex: isoler les utilisateurs ayant cliqué < 4 fois pour voir si l'algorithme Hybride ou la Popularité performent mieux que l'ALS).

---
*(Note : Le fichier `04_modelisation.ipynb` contient nos premières ébauches exploratoires et n'est plus utilisé activement dans ce pipeline de benchmark structuré).*
