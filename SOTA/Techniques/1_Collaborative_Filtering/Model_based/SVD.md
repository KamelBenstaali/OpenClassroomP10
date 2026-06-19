# Filtrage Collaboratif Model-Based : SVD (Singular Value Decomposition)

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

### 4. Avantages (Pros) 👍
* **Surmonte la Sparsity :** Gère très bien les matrices contenant énormément de valeurs manquantes (zéros).
* **Précision historique :** C'est l'algorithme qui a remporté le fameux concours "Netflix Prize", reconnu pour son excellente précision sur des jeux de données avec notations.
* **Inférence ultra-rapide :** Une fois le modèle entraîné, calculer la recommandation est un simple produit scalaire matriciel (instantané).

### 5. Inconvénients et Limites (Cons) 👎
* **Sensibilité aux données implicites :** Historiquement, le SVD classique de base gère assez mal l'Implicit Feedback (car le fait qu'il n'y ait pas de clic ne veut pas dire "je déteste", mais "je n'ai pas encore vu").
* **Opacité (Boîte Noire) :** Impossible de justifier clairement une recommandation à l'utilisateur car les "facteurs latents" sont des vecteurs mathématiques sans libellé humain compréhensible.
* **Cold-Start :** Reste inefficace pour les nouveaux articles non évalués et les nouveaux utilisateurs sans clics.

### 6. Métriques d'évaluation pertinentes
* **Métriques de Prédiction (Erreur) :** RMSE (Root Mean Squared Error) et MAE.
* **Métriques de Classement (Ranking) :** Hit Ratio, Precision@K, NDCG.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'entraînement par descente de gradient peut être lourd sur des données massives. L'inférence, en revanche, est très frugale et parfaite pour le Cloud (Serverless).
* **Complexité :** La mise à jour (l'arrivée massive de nouveaux utilisateurs) nécessite souvent un ré-entraînement complet du modèle.

### 8. Cas d'usage Typiques & Exemples réels
* Recommandation de films sur Netflix ou d'articles e-commerce (lorsque les utilisateurs laissent une note, un pouce en l'air, ou un avis clair sur 5 étoiles).

### 9. Bibliothèques et Outils (Implémentation)
* La librairie Python `scikit-surprise` (classe `SVD`) est l'implémentation de référence.
