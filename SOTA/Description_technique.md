Pour avoir un **État de l'Art (SOTA)** rigoureux, structuré et facile à comparer, il est recommandé d'utiliser un modèle (template) commun pour tous tes fichiers d'algorithmes. 

Voici les critères essentiels que je te conseille d'inclure systématiquement dans chaque document pour bien les décrire et les comparer :

### 1. Principe de base (L'intuition)
* **Description en une phrase :** Quel est le concept principal ? (vulgarisation).
* **Comment ça marche ?** Une explication logique et simple de l'approche (ex: "Trouver des utilisateurs qui ont les mêmes goûts que moi, puis me recommander ce qu'ils ont aimé").

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :** La formule clé ou l'algorithme de base (ex: formule de la Similarité Cosinus, principe de la factorisation SVD, architecture du réseau de neurones).
* *Tu peux y inclure de petites formules mathématiques avec la syntaxe LaTeX (`$$ formula $$`).*

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Matrice d'interactions (User-Item ratings/clics)
  * Métadonnées des utilisateurs (âge, localisation)
  * Caractéristiques des items (texte, catégories, images)
  * Données contextuelles (heure, météo, device)

### 4. Avantages (Pros) 👍
* Pourquoi choisirait-on cette méthode ? (ex: facile à implémenter, facilement explicable, gère bien les nouveaux items, capture les relations non-linéaires complexes).

### 5. Inconvénients et Limites (Cons) 👎
* Les points faibles classiques à mentionner absolument dans les recos :
  * **Problème de démarrage à froid (Cold-Start) :** L'algorithme survit-il sans données historiques pour un nouvel utilisateur ou un nouvel item ?
  * **Sparsity (rareté des données) :** Que se passe-t-il si la matrice est remplie à 99% de zéros ?
  * **Effet Bulle de Filtre (Filter Bubble / Over-specialization) :** L'algorithme a-t-il tendance à enfermer l'utilisateur dans ses propres goûts sans proposer de nouveauté ?

### 6. Métriques d'évaluation pertinentes
Comment mesure-t-on le succès de cet algorithme ?
* **Métriques de Prédiction (Erreur) :** MAE, RMSE (plutôt pour la prédiction de notes exactes).
* **Métriques de Classement (Ranking) :** Precision@K, Recall@K, NDCG, MAP (pour l'ordre de pertinence du Top-K recommandé).
* **Métriques "Business" ou non-précision :** Diversité, Sérendipité (capacité à surprendre agréablement), Couverture (Catalogue Coverage).

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'algorithme est-il lent à entraîner ? Est-il rapide pour servir une recommandation en temps réel ?
* **Complexité :** Comment se comporte-t-il si on passe de 10 000 à 10 millions d'utilisateurs/items ?

### 8. Cas d'usage Typiques & Exemples réels
* **Quand l'utiliser ?** (ex: Recommandation d'articles d'actualités fraîchement publiés = Content-based. Recommandation de films sur Netflix = Hybrid/Collaboratif).

### 9. Bibliothèques et Outils (Implémentation)
* **Quelles librairies Python utiliser ?** (ex: `scikit-learn` pour la Similarité Cosinus, `Gensim` pour LDA, `Surprise` pour le filtrage collaboratif classique, `LightFM`, `TensorFlow Recommenders`).

