# Plan d'Exécution

## 1. Contexte et Synthèse du Projet
- Définition du contexte de la mission (Start-up My Content).
- Identification de la fonctionnalité critique (recommandation de 5 articles).

## 2. Configuration de l'Environnement
- **Installation des dépendances **

## 3. Préparation et Chargement des Données
- Mise en place de l'environnement (Montage Google Drive).
- Extraction des archives ZIP (`news-portal-user-interactions-by-globocom.zip` et `clicks.zip`).
- Chargement des 3 fichiers clés en mémoire :
  - `clicks_sample.csv` (pour le MVP).
  - `articles_metadata.csv` (métadonnées).
  - `articles_embeddings.pickle` (matrice des vecteurs).

## 4. Modélisation : Approche Content-Based Filtering (Similarité)
- **Choix technique retenu : Similarité Cosinus** sur les embeddings (plutôt que LDA).
- **Justification :** Utilisation optimale de `articles_embeddings.pickle` fournis (après réduction de dimension via ACP pour limiter la mémoire sur Azure Functions). Plus rapide et pertinent que l'extraction de thèmes (LDA).
- Définition d'une fonction pour récupérer l'historique de lecture d'un utilisateur cible (`user_id`).
- Calcul du "profil utilisateur" (ex: moyenne des embeddings ACP des articles qu'il a lus).
- Calcul de la similarité cosinus entre le profil utilisateur et tous les autres articles du catalogue.
- Tri et recommandation des 5 articles les plus pertinents (exclusion des articles déjà lus).

## 5. Modélisation : Approche Collaborative Filtering (Model-Based implicite)
- **Choix technique retenu : Algorithme ALS (Alternating Least Squares)** via la librairie `implicit`.
- **Justification :** 
  - **Nature des données :** Nous n'avons pas de notes explicites (ex: 1 à 5 étoiles), mais uniquement des historiques de clics (**Implicit Feedback**). L'algorithme ALS est spécialement optimisé pour traiter ce type de données (en utilisant le clic comme score de "confiance"), contrairement au modèle SVD standard (comme celui de `scikit-surprise`) qui est pensé pour des notes explicites.
  - **Performance :** L'inférence rapide par produit scalaire répond parfaitement aux contraintes de l'architecture Serverless (MVP Azure Functions).
- Création d'une matrice creuse (sparse matrix) User-Item basée sur les interactions.
- Utilisation de la librairie `implicit` pour entraîner le modèle ALS.
- Génération de recommandations rapides pour prédire la pertinence des articles non lus.

## 6. Évaluation et Choix du Modèle (MVP)
Puisque nous n'avons pas de notes (données implicites), nous ne pouvons pas utiliser des métriques classiques d'erreur (comme le RMSE). Nous allons utiliser des métriques de classement (Ranking) sur un jeu de test :

- **Séparation Train / Test :** Pour chaque utilisateur, nous allons cacher une partie de ses clics récents (pour le test) et entraîner le modèle sur le reste.
- **Métriques Quantitatives :** 
  - **Precision@5** : Parmi les 5 articles recommandés, combien ont été réellement cliqués par l'utilisateur dans le jeu de test ?
  - **Recall@5** : Sur tous les articles que l'utilisateur a cliqués dans le test, quel pourcentage se trouve dans notre Top 5 ?
  - **NDCG@5** : Évalue si l'article le plus pertinent est placé en haut de la liste des 5 recommandations.
- **Évaluation Qualitative :** Inspection manuelle sur quelques `user_id` pour voir si les catégories et thèmes recommandés font sens par rapport à l'historique (Sérendipité et Diversité).
- **Évaluation Technique (Azure Functions) :** 
  - Temps d'inférence (doit être quasi-instantané).
  - Poids des matrices/modèles en mémoire (doit respecter la limite du plan Serverless).
- **Sélection :** Comparaison finale entre Content-Based (Similarité) et Collaborative Filtering (ALS) et choix du modèle pour la production.
