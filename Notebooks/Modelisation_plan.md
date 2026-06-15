# Plan d'Exécution (Basé sur p10_exemple.ipynb)

Voici le plan détaillé des instructions qui ont été exécutées dans le notebook d'exemple `p10_exemple.ipynb` :

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

## 4. Modélisation : Approche Content-Based filtering
- Définition d'une fonction pour récupérer l'historique de lecture d'un utilisateur cible (`user_id`).
- Calcul du "profil utilisateur" (moyenne des embeddings ACP des articles qu'il a lus).
- Calcul de la similarité cosinus entre le profil utilisateur et tous les autres articles du catalogue.
- Tri et recommandation des 5 articles les plus pertinents (exclusion des articles déjà lus).

## 5. Modélisation : Approche Collaborative Filtering
- Création d'une matrice User-Item basée sur les interactions (clics).
- Utilisation de la librairie `scikit-surprise` (ex: modèle SVD ou KNN) pour trouver des similarités de comportement entre utilisateurs.
- Génération de recommandations basées sur les lectures des utilisateurs "voisins".

## 6. Évaluation et Choix du Modèle (MVP)
- Exécution de quelques prédictions manuelles de test sur différents `user_id`.
- Comparaison des deux approches (Content-Based vs Collaborative Filtering).
- Sélection de l'algorithme retenu pour le développement de la fonctionnalité finale (Azure Function).
