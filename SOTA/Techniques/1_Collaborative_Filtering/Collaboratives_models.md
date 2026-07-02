# Les Modèles de Filtrage Collaboratif

Ce document regroupe les différentes approches algorithmiques du filtrage collaboratif explorées dans ce projet.

---

## 1. Approche Memory-Based (K-Nearest Neighbors)
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



### 4. Métriques d'évaluation pertinentes
* **Métriques de Prédiction (Erreur) :** RMSE (Root Mean Squared Error), MAE (Mean Absolute Error) pour évaluer la précision des notes prédites.
* **Métriques de Classement (Ranking) :** Precision@K, NDCG pour la qualité du top des recommandations.

### 5. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'entraînement est inexistant (approche "lazy"), mais l'inférence (calculer les voisins et prédire) peut être extrêmement coûteuse en temps réel sur de très grosses matrices.
* **Complexité :** L'approche User-User scale très mal si le nombre d'utilisateurs explose ($O(U^2)$). L'approche Item-Item est généralement préférée en production car le catalogue d'items est plus stable et la matrice de similarité item-item peut être pré-calculée.

### 6. Bibliothèques et Outils (Implémentation)
* `Surprise` (En Python, excellente bibliothèque incluant `KNNBasic`, `KNNWithMeans`).
* `scikit-learn` (`NearestNeighbors`).

---

## 2. Approche Model-Based : SVD (Singular Value Decomposition)
### 1. Principe de base (L'intuition)
* **Description en une phrase :** Décomposer la grande matrice de recommandations en deux plus petites matrices (profils utilisateurs et caractéristiques d'éléments) pour identifier les facteurs cachés influençant les préférences.
* **Comment ça marche ?** L'algorithme estime que le goût d'un utilisateur pour un article dépend d'un nombre réduit de "facteurs latents" abstraits (ex: le ton de l'article, la longueur, la catégorie). SVD compresse les données pour faire ressortir ces facteurs et prédire comment un utilisateur réagirait à un article non lu.

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :** 
  * On décompose la matrice des interactions $R$ (taille $U \times I$) en deux matrices de facteurs latents $P$ (profils utilisateurs) et $Q$ (caractéristiques des items).
  * Le score prédit $\hat{r}_{ui}$ de l'utilisateur $u$ pour l'item $i$ est le produit scalaire : $\hat{r}_{ui} = p_u \cdot q_i$.
  * On optimise ces matrices généralement par **Descente de Gradient Stochastique (SGD)** en minimisant l'erreur entre le vrai score et $\hat{r}_{ui}$.

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Par conception, SVD demande une matrice d'interactions avec des **notes explicites** (Explicit Feedback) de type 1 à 5 étoiles (rating).
  * Pour l'appliquer sur des données implicites (comme de simples clics), il est obligatoire de "fabriquer" un pseudo-score (ex: 1 clic = 1 point) via une étape de prétraitement des données.



### 4. Métriques d'évaluation pertinentes
* **Métriques de Prédiction (Erreur) :** RMSE (Root Mean Squared Error) et MAE.
* **Métriques de Classement (Ranking) :** Hit Ratio, Precision@K, NDCG.

### 5. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'entraînement par descente de gradient peut être lourd sur des données massives. L'inférence, en revanche, est très frugale et parfaite pour le Cloud (Serverless).
* **Complexité :** La mise à jour (l'arrivée massive de nouveaux utilisateurs) nécessite souvent un ré-entraînement complet du modèle.

### 6. Bibliothèques et Outils (Implémentation)
* La librairie Python `scikit-surprise` (classe `SVD`) est l'implémentation de référence.

---

## 3. Approche Model-Based : ALS (Alternating Least Squares)
### 1. Principe de base (L'intuition)
* **Description en une phrase :** Une méthode de factorisation de matrices spécialement conçue et optimisée pour analyser les comportements passifs (clics, temps d'écran) plutôt que les notes explicites.
* **Comment ça marche ?** Comme SVD, l'algorithme décompose la grande matrice en facteurs latents. Mais au lieu de tout calculer d'un coup avec une descente de gradient, ALS fixe alternativement les "utilisateurs" pour résoudre les "articles", puis fixe les "articles" pour résoudre les "utilisateurs". De plus, il traite l'absence d'interaction non pas comme une note nulle, mais comme un manque de données, et utilise le nombre de clics comme un score de "confiance".

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :**
  * Le score prédit est $\hat{r}_{ui} = p_u \cdot q_i$.
  * La fonction d'erreur/coût est modifiée pour inclure une notion de **Confiance** ($c_{ui} = 1 + \alpha \cdot r_{ui}$). Plus l'utilisateur a cliqué souvent sur un type d'article, plus l'algorithme a "confiance" dans le fait qu'il aime ce contenu.
  * Optimisation "Alternée" : À chaque itération, on gèle $P$ et on calcule $Q$ mathématiquement (moindres carrés), puis on gèle $Q$ et on calcule $P$.

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Spécialement conçu pour l'**Implicit Feedback** (retours implicites) : clics, actes d'achat, nombre d'écoutes, durées de lecture.
  * Ingeste une grande matrice creuse (sparse matrix).



### 4. Métriques d'évaluation pertinentes
* **Métriques de Classement (Ranking) :** Contrairement à SVD, on évite le RMSE (car on ne prédit pas une "note" exacte). On évalue uniquement le classement relatif du catalogue : **Hit Ratio@K, NDCG, Precision@K, MAP**.

### 5. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'entraînement est hautement parallélisable et rapide. L'inférence est quasi instantanée.
* **Complexité :** L'une des meilleures scalabilités du marché pour les environnements Big Data.

### 6. Bibliothèques et Outils (Implémentation)
* La librairie Python `implicit` (contenant la classe `AlternatingLeastSquares` ultra-optimisée en Cython/C++ sous le capot).
* `Apache Spark MLlib` pour les environnements de calcul distribué massif.
