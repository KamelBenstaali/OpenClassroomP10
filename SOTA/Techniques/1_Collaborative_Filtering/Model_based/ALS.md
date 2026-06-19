# Filtrage Collaboratif Model-Based : ALS (Alternating Least Squares)

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

### 4. Avantages (Pros) 👍
* **Le Roi des données implicites :** C'est le standard absolu de l'industrie quand on ne possède pas d'étoiles/notes (ce qui est notre cas avec les clics du portail Globo).
* **Calcul Parallélisable :** La méthode de résolution alternée permet de distribuer facilement les calculs sur plusieurs processeurs (CPU) ou plusieurs machines (Spark), rendant l'entraînement beaucoup plus rapide que la descente de gradient sur les grosses bases de données.
* **Latence d'inférence exceptionnelle :** Extrêmement rapide pour générer un Top 5 en production via des opérations C++ vectorisées.

### 5. Inconvénients et Limites (Cons) 👎
* **Boîte Noire (Opacité) :** Même défaut que SVD, les "facteurs latents" ne sont pas interprétables métier.
* **Cold-Start total :** Impossible de recommander un article qui vient d'être publié dans la seconde (il a 0 clic, donc il n'existe pas dans la matrice de base). Ne gère pas les nouveaux utilisateurs sans historique.
* **Modèle figé :** La matrice doit être reconstruite et le modèle réentraîné régulièrement pour proposer les tout nouveaux articles.

### 6. Métriques d'évaluation pertinentes
* **Métriques de Classement (Ranking) :** Contrairement à SVD, on évite le RMSE (car on ne prédit pas une "note" exacte). On évalue uniquement le classement relatif du catalogue : **Hit Ratio@K, NDCG, Precision@K, MAP**.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'entraînement est hautement parallélisable et rapide. L'inférence est quasi instantanée.
* **Complexité :** L'une des meilleures scalabilités du marché pour les environnements Big Data.

### 8. Cas d'usage Typiques & Exemples réels
* Recommandation musicale sur Spotify (basée sur le nombre implicite d'écoutes).
* Recommandation d'articles ou de produits e-commerce sans système de notation.

### 9. Bibliothèques et Outils (Implémentation)
* La librairie Python `implicit` (contenant la classe `AlternatingLeastSquares` ultra-optimisée en Cython/C++ sous le capot).
* `Apache Spark MLlib` pour les environnements de calcul distribué massif.
