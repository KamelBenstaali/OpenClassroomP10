# Filtrage Collaboratif Model-Based (Factorisation de Matrices)

### 1. Principe de base (L'intuition)
* **Description en une phrase :** Entraîner un modèle de Machine Learning pour découvrir des "caractéristiques latentes" (cachées) expliquant pourquoi un utilisateur aime un item.
* **Comment ça marche ?** Au lieu de chercher des voisins directs, l'algorithme "compresse" la grande matrice Utilisateur-Item remplie de trous en deux petites matrices (une pour les utilisateurs, une pour les items). La multiplication de ces deux petites matrices permet de prédire (remplir) les trous.

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :**
  * **SVD (Singular Value Decomposition) / Matrix Factorization :** On décompose la matrice des notes $R$ en deux matrices de facteurs latents $P$ (utilisateurs) et $Q$ (items).
  * La note prédite $\hat{r}_{ui}$ de l'utilisateur $u$ pour l'item $i$ est le produit scalaire : $\hat{r}_{ui} = p_u \cdot q_i$.
  * On optimise ces matrices via l'algorithme d'**ALS (Alternating Least Squares)** ou par **Descente de Gradient Stochastique (SGD)** pour minimiser l'erreur entre les notes réelles et les notes prédites.

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Une matrice d'interactions Utilisateur-Item (Notes, temps de visionnage, clics).
  * Gère très bien les retours implicites (Implicit Feedback) avec des approches spécifiques (ex: ALS implicite).

### 4. Avantages (Pros) 👍
* **Surmonte le problème de Sparsity :** Bien meilleur que l'approche Memory-Based quand la matrice est très creuse.
* **Performances prédictives supérieures :** Capte des relations subtiles et non linéaires (les fameux "facteurs latents" comme le genre d'un film, même s'ils ne sont pas nommés).
* Extrêmement rapide au moment de l'inférence : prédire une note n'est qu'un simple produit scalaire entre deux petits vecteurs.

### 5. Inconvénients et Limites (Cons) 👎
* **Moins explicable :** Impossible de dire précisément à l'utilisateur *pourquoi* on lui recommande cela (les "facteurs latents" sont des concepts mathématiques abstraits, pas des catégories en clair).
* **Cold-Start :** Reste vulnérable au démarrage à froid (nouveaux utilisateurs / nouveaux items sans historique).
* **Modèle figé :** Doit être ré-entraîné (ou mis à jour périodiquement) pour prendre en compte les toutes nouvelles notes ou nouveaux utilisateurs de manière optimale.

### 6. Métriques d'évaluation pertinentes
* **Métriques de Prédiction (Erreur) :** RMSE (Root Mean Squared Error) est la métrique reine ici (rendue célèbre par le Netflix Prize).
* **Métriques de Classement (Ranking) :** Precision@K, NDCG, MAP.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'entraînement peut être long sur de très gros datasets. Cependant, des algorithmes comme ALS sont hautement parallélisables (Spark). L'inférence est instantanée.
* **Complexité :** Très bonne scalabilité globale. C'est le standard de l'industrie pour les gros volumes.

### 8. Cas d'usage Typiques & Exemples réels
* Le concours "Netflix Prize" (2006-2009) a été remporté par des variantes avancées de SVD.
* Spotify l'utilise (souvent via ALS implicite) pour recommander des musiques en fonction des historiques d'écoute de millions d'utilisateurs.

### 9. Bibliothèques et Outils (Implémentation)
* `Surprise` (Algorithme `SVD`, `SVDpp`, `NMF`).
* `Implicit` (Excellente librairie Python optimisée en C++ pour l'ALS sur des retours implicites).
* `Apache Spark MLlib` (Pour faire de l'ALS à très grande échelle sur des clusters Big Data).
