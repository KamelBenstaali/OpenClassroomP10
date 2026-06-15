# Latent Dirichlet Allocation (LDA)

### 1. Principe de base (L'intuition)
* **Description en une phrase :** Un modèle probabiliste qui découvre automatiquement les thèmes (topics) cachés dans une large collection de textes.
* **Comment ça marche ?** L'algorithme part du principe que chaque document est un mélange de plusieurs "thèmes" et que chaque thème est un mélange de "mots". Il analyse les co-occurrences de mots pour regrouper les documents similaires sous des profils thématiques.

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :** LDA est un modèle génératif bayésien. Il utilise la distribution de Dirichlet pour modéliser deux distributions probabilistes :
  1. La probabilité des thèmes par document ($\theta$).
  2. La probabilité des mots par thème ($\phi$).
* L'objectif est d'inverser ce processus génératif via des algorithmes d'inférence (ex: Échantillonnage de Gibbs ou Variational Bayes) pour trouver les thèmes à partir des mots observés.

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Un corpus de documents textuels (descriptions de produits, avis, articles de presse, synopsis de films).
  * Les textes doivent être prétraités (tokenization, suppression des stop-words, lemmatisation).

### 4. Avantages (Pros) 👍
* Capture la "sémantique" latente : comprend que "voiture" et "automobile" appartiennent au même thème, contrairement à une simple recherche par mots-clés (TF-IDF).
* Non supervisé : pas besoin d'annoter manuellement les catégories ou les tags des documents.
* Fournit une représentation dense (un petit vecteur de probabilités de thèmes) au lieu d'un immense vecteur clairsemé (vocabulaire entier).

### 5. Inconvénients et Limites (Cons) 👎
* Le nombre de thèmes ($K$) doit être défini à l'avance par l'humain (hyperparamètre difficile à régler).
* Les thèmes générés ne sont pas toujours facilement interprétables par un humain (ex: Thème 1 = "pomme, ordinateur, souris", Thème 2 = "pomme, fruit, arbre").
* Lent à entraîner sur de très gros corpus par rapport à des méthodes plus simples (TF-IDF).

### 6. Métriques d'évaluation pertinentes
* **Cohérence des thèmes (Topic Coherence) :** Mesure si les mots les plus probables d'un thème ont sémantiquement du sens ensemble.
* **Perplexité (Perplexity) :** Mesure la capacité du modèle à prédire un échantillon de documents non vus (plus bas = meilleur).
* **Métriques de Recommandation classiques :** Precision@K, Recall@K une fois les vecteurs de thèmes utilisés pour le filtrage par contenu.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** L'entraînement est coûteux en temps de calcul et en mémoire (plusieurs passes sur tout le corpus). L'inférence (trouver les thèmes d'un nouveau document) est rapide.
* **Complexité :** Assez gourmand. Il est souvent nécessaire d'utiliser des implémentations parallélisées ou adaptées au Big Data pour des millions de documents.

### 8. Cas d'usage Typiques & Exemples réels
* Recommandation d'articles scientifiques (ex: arXiv, Google Scholar) basée sur les résumés.
* Classification automatique de tickets support pour les orienter vers le bon service.
* Enrichissement du profil utilisateur : L'utilisateur lit 80% d'articles du thème 4 et 20% du thème 1.

### 9. Bibliothèques et Outils (Implémentation)
* `Gensim` (L'implémentation de référence en Python, très optimisée : `LdaModel`).
* `scikit-learn` (`LatentDirichletAllocation`).
* `pyLDAvis` (Pour la visualisation interactive des thèmes générés).
