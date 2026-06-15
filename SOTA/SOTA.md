# État de l'Art : Les Systèmes de Recommandation

Les systèmes de recommandation sont des algorithmes visant à suggérer des éléments pertinents (articles, films, produits) aux utilisateurs en fonction de leurs préférences explicites ou implicites. Ils sont divisés en plusieurs grandes familles d'approches.

Ce document résume les principales techniques existantes (State of the Art - SOTA) : le filtrage basé sur le contenu, le filtrage collaboratif, et les approches hybrides.

---

## 1. L'Approche Basée sur le Contenu (Content-Based Filtering)

L'approche basée sur le contenu s'appuie sur les **caractéristiques des éléments (items)** et le profil de l'utilisateur. Le principe fondamental est : *"Recommander des articles similaires à ceux que l'utilisateur a aimés ou consultés par le passé."*

### Fonctionnement :
- **Représentation des items :** Chaque article est décrit par un vecteur de caractéristiques (mots-clés, catégories, ou des embeddings générés par des modèles de traitement du langage naturel comme Word2Vec, BERT, etc.).
- **Profil utilisateur :** Un profil utilisateur est créé en agrégeant les caractéristiques des articles avec lesquels il a interagi.
- **Calcul de similarité :** L'algorithme calcule une distance (souvent la *similarité cosinus*) entre le profil de l'utilisateur et les articles candidats.

### ✅ Avantages :
- **Indépendance vis-à-vis des autres utilisateurs :** Pas besoin d'une large base d'utilisateurs pour commencer à faire de bonnes recommandations.
- **Pas de Cold Start (démarrage à froid) pour les nouveaux articles :** Dès qu'un nouvel article est publié, ses métadonnées ou embeddings permettent de le recommander instantanément.
- **Transparence :** Les recommandations sont faciles à expliquer ("Parce que vous avez lu des articles sur la technologie...").

### ❌ Inconvénients :
- **Bulle de filtres (Over-specialization) :** Le système enferme l'utilisateur dans ce qu'il connaît déjà et manque de "sérendipité" (incapacité à faire découvrir de nouvelles thématiques).
- **Cold Start pour les nouveaux utilisateurs :** Sans historique de lecture, il est impossible de générer un profil pour un nouvel utilisateur.

---

## 2. Le Filtrage Collaboratif (Collaborative Filtering)

Le filtrage collaboratif repose uniquement sur les **interactions passées (clics, notes, temps de lecture)** entre les utilisateurs et les items, sans avoir besoin de connaître le contenu des articles. Le principe est : *"Si deux utilisateurs ont eu le même comportement par le passé, ils auront probablement les mêmes goûts à l'avenir."*

Cette approche se divise en deux sous-catégories principales :

### A. Memory-Based (ou Neighborhood-Based)
Ces méthodes utilisent directement la matrice d'interactions Utilisateurs-Items pour trouver des "voisins" via des mesures de similarité (Corrélation de Pearson, Cosinus).
- **User-Based Collaborative Filtering (UBCF) :** On trouve des utilisateurs similaires à l'utilisateur cible (ses "voisins") et on lui recommande les articles que ces voisins ont aimés.
- **Item-Based Collaborative Filtering (IBCF) :** On trouve des articles similaires à ceux que l'utilisateur a déjà lus (la similarité entre deux articles se basant sur le fait qu'ils ont été lus par les mêmes personnes). L'IBCF est souvent plus stable et scalable que l'UBCF.

### B. Model-Based
Au lieu de calculer des distances directes, ces méthodes construisent un modèle mathématique à partir de la matrice d'interactions (souvent très creuse/sparse) pour prédire les valeurs manquantes.
- **Factorisation de Matrice (Matrix Factorization) :** Des algorithmes comme SVD (Singular Value Decomposition) ou ALS (Alternating Least Squares) décomposent la grande matrice d'interactions en deux matrices plus petites (vecteurs latents pour les utilisateurs et les items).
- **Deep Learning :** Des approches comme les Autoencodeurs ou Neural Collaborative Filtering (NCF) capturent des relations non-linéaires complexes.

### ✅ Avantages :
- **Sérendipité :** Permet à l'utilisateur de découvrir des articles complètement différents de ses lectures habituelles, car basés sur l'intelligence collective.
- **Pas besoin de métadonnées :** Ne requiert aucune analyse du texte des articles.

### ❌ Inconvénients :
- **Problème de la matrice creuse (Sparsity) :** Beaucoup d'articles ne sont lus que par un nombre infime d'utilisateurs.
- **Cold Start global :** Impossible de recommander un nouvel article qui n'a jamais été lu (Cold Start Item), ni de recommander à un nouvel utilisateur sans historique (Cold Start User).
- **Scalabilité :** Les méthodes basées sur la mémoire coûtent très cher en temps de calcul lorsque la base de données devient énorme.

---

## 3. Les Approches Hybrides

Pour pallier les défauts respectifs du Content-Based (Bulle de filtre) et du Collaborative Filtering (Cold start des nouveaux articles), les systèmes de recommandation modernes combinent souvent les deux.

- **Combinaison pondérée :** On calcule séparément les recommandations des deux systèmes et on pondère les scores finaux.
- **Cascade :** Le premier système filtre une large sélection d'articles, et le deuxième système affine ce sous-ensemble.
- **Feature augmentation :** On injecte les représentations basées sur le contenu (comme les embeddings de vos articles) comme "features" supplémentaires dans un modèle de Collaborative Filtering complexe (ex: LightFM, Factorization Machines).

---

## 🎯 Conclusion & Application à notre projet MVP ("My Content")

Dans le cadre de votre application, nous disposons de deux ensembles de données clés :
1. Les interactions (`clicks`) $\rightarrow$ Permettrait du **Collaborative Filtering**.
2. Le contenu via les `articles_embeddings` $\rightarrow$ Permettrait du **Content-Based Filtering**.

Pour une **architecture Serverless (Azure Functions)** avec des contraintes de mémoire et de temps de réponse pour un MVP, l'approche **Content-Based** avec recherche de similarité cosinus sur les embeddings réduits par ACP est souvent la solution technique la plus robuste pour démarrer, car :
- Elle résout parfaitement le problème d'intégration des nouveaux articles.
- Elle est très rapide à exécuter "à la volée" sans nécessiter de ré-entraîner de lourdes matrices mathématiques.
