# Filtrage Collaboratif Memory-Based (Voisinage)

### 1. Principe de base (L'intuition)
* **Description en une phrase :** Recommander des items en se basant sur les similarités directes entre les historiques des utilisateurs ou les interactions avec les items.
* **Comment ça marche ?** 
  * **User-User :** "Les utilisateurs qui te ressemblent (qui ont aimé les mêmes choses que toi) ont aussi aimé l'item X, donc on te recommande X."
  * **Item-Item :** "Tu as aimé l'item Y. Les utilisateurs qui ont aimé Y ont souvent aussi aimé l'item Z, donc on te recommande Z."

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :** Utilisation des algorithmes de Plus Proches Voisins (K-Nearest Neighbors / KNN).
  * On calcule une matrice de similarité (Cosinus, Corrélation de Pearson) entre toutes les paires d'utilisateurs (ou d'items).
  * Pour prédire la note d'un utilisateur pour un item, on fait la moyenne pondérée des notes données à cet item par les $K$ voisins les plus similaires.

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Une matrice d'interactions Utilisateur-Item (Ratings explicites comme des étoiles, ou implicites comme des clics/achats).
  * Aucune métadonnée ou attribut sur l'item ou l'utilisateur n'est nécessaire.

### 4. Avantages (Pros) 👍
* Facile à comprendre, à implémenter, et extrêmement transparent/explicable (ex: "Nous vous recommandons ceci car vous avez aimé cela").
* Pas besoin de connaitre le contenu ou les attributs des items.
* Ajout facile de nouvelles données : une nouvelle note met à jour les similarités sans avoir à "ré-entraîner" un modèle complexe.

### 5. Inconvénients et Limites (Cons) 👎
* **Sparsity (Matrice creuse) :** Si la matrice est vide à 99% (les utilisateurs notent peu de choses), il est très dur de trouver des voisins ayant des items en commun.
* **Cold-Start :** Impossible de recommander un nouvel item qui n'a jamais été noté (Item Cold-Start) ou à un nouvel utilisateur qui n'a rien noté (User Cold-Start).
* **Biais de popularité (Popularity Bias) :** Les items très populaires dominent souvent les recommandations, cachant les items de "longue traîne".

### 6. Métriques d'évaluation pertinentes
* **Métriques de Prédiction (Erreur) :** RMSE (Root Mean Squared Error), MAE (Mean Absolute Error) pour évaluer la précision des notes prédites.
* **Métriques de Classement (Ranking) :** Precision@K, NDCG pour la qualité du top des recommandations.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'entraînement est inexistant (approche "lazy"), mais l'inférence (calculer les voisins et prédire) peut être extrêmement coûteuse en temps réel sur de très grosses matrices.
* **Complexité :** L'approche User-User scale très mal si le nombre d'utilisateurs explose ($O(U^2)$). L'approche Item-Item est généralement préférée en production car le catalogue d'items est plus stable et la matrice de similarité item-item peut être pré-calculée.

### 8. Cas d'usage Typiques & Exemples réels
* Recommandations E-commerce de type "Ceux qui ont acheté ceci ont aussi acheté cela" (Amazon a popularisé l'Item-Item CF en 2003).

### 9. Bibliothèques et Outils (Implémentation)
* `Surprise` (En Python, excellente bibliothèque incluant `KNNBasic`, `KNNWithMeans`).
* `scikit-learn` (`NearestNeighbors`).
