# Similarité (Mesures de distance)

### 1. Principe de base (L'intuition)
* **Description en une phrase :** Évaluer mathématiquement à quel point deux items (ou deux utilisateurs) se ressemblent en se basant sur leurs caractéristiques.
* **Comment ça marche ?** On représente les items sous forme de vecteurs (listes de nombres) dans un espace à $N$ dimensions. Plus les vecteurs sont "proches" dans cet espace, plus les items sont considérés comme similaires et peuvent être recommandés.

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :**
  * **Similarité Cosinus :** Mesure l'angle entre deux vecteurs. Très efficace pour les textes (TF-IDF).
    $$ \text{Cosine}(A, B) = \frac{A \cdot B}{||A|| \times ||B||} $$
  * **Indice de Jaccard :** Mesure le chevauchement entre deux ensembles (intersection sur union). Idéal pour des attributs binaires (ex: tags).
    $$ \text{Jaccard}(A, B) = \frac{|A \cap B|}{|A \cup B|} $$
  * **Distance Euclidienne :** Mesure la distance en ligne droite classique. Souvent sensible à la magnitude (la taille des vecteurs).

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Caractéristiques des items numérisées (vecteurs TF-IDF, embeddings de mots, variables One-Hot Encoding pour les catégories).

### 4. Avantages (Pros) 👍
* Facile à implémenter et à comprendre.
* Pas de problème de démarrage à froid pour les nouveaux items (Cold-Start Item) : dès qu'un item a des attributs, on peut calculer sa similarité.
* Totalement indépendant des autres utilisateurs (pas besoin d'une grosse base d'utilisateurs).

### 5. Inconvénients et Limites (Cons) 👎
* **Cold-Start User :** Un nouvel utilisateur sans historique n'aura pas de recommandations personnalisées.
* **Over-specialization (Bulle de filtre) :** Ne recommande que des choses "exactement pareilles" à ce que l'utilisateur connaît déjà. Ne permet pas la découverte inattendue (sérendipité faible).
* Les mesures classiques luttent pour capturer la sémantique complexe (ex: "Iron Man" et "Avengers" pourraient ne pas partager les mêmes mots-clés exacts sans des techniques plus avancées).

### 6. Métriques d'évaluation pertinentes
* **Métriques de Classement (Ranking) :** Precision@K, Recall@K (L'item pertinent était-il dans le Top K des items les plus similaires ?).
* **Diversité / Sérendipité :** À surveiller de près car cette méthode a tendance à obtenir de mauvais scores sur ces métriques.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** Pas vraiment "d'entraînement". L'inférence (calcul de similarité au moment de la requête) peut être très lente ($O(N)$) s'il y a des millions d'items.
* **Complexité :** Des techniques d'approximation (ex: FAISS, LSH - Locality Sensitive Hashing) sont nécessaires pour passer à l'échelle sur de gros catalogues.

### 8. Cas d'usage Typiques & Exemples réels
* Recommandation de "Produits similaires" sur un site E-commerce (ex: Amazon "Les clients ayant vu cet article ont aussi regardé...").
* Recommandation d'articles de blog ou de presse basés sur le texte de l'article en cours de lecture.

### 9. Bibliothèques et Outils (Implémentation)
* `scikit-learn` (`cosine_similarity`, `pairwise_distances`)
* `SciPy` (modules de distances spatiales)
* `FAISS` de Meta (pour la recherche de similarité vectorielle à très grande échelle)
