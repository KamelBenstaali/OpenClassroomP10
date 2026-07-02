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


### 6. Métriques d'évaluation pertinentes
* **Métriques de Classement (Ranking) :** Precision@K, Recall@K (L'item pertinent était-il dans le Top K des items les plus similaires ?).
* **Diversité / Sérendipité :** À surveiller de près car cette méthode a tendance à obtenir de mauvais scores sur ces métriques.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** Pas vraiment "d'entraînement". L'inférence (calcul de similarité au moment de la requête) peut être très lente ($O(N)$) s'il y a des millions d'items.
* **Complexité :** Des techniques d'approximation (ex: FAISS, LSH - Locality Sensitive Hashing) sont nécessaires pour passer à l'échelle sur de gros catalogues.

### 8. Bibliothèques et Outils (Implémentation)
* `scikit-learn` (`cosine_similarity`, `pairwise_distances`)
* `SciPy` (modules de distances spatiales)
* `FAISS` de Meta (pour la recherche de similarité vectorielle à très grande échelle)
