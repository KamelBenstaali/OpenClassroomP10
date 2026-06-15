# Systèmes Hybrides

### 1. Principe de base (L'intuition)
* **Description en une phrase :** Combiner deux ou plusieurs algorithmes de recommandation pour tirer parti de leurs forces respectives et annuler leurs faiblesses.
* **Comment ça marche ?** Si le filtrage collaboratif (CF) est bon pour la précision mais souffre du cold-start, et que le Content-Based (CB) gère bien le cold-start mais manque de sérendipité, on les fusionne. Cela peut se faire en pondérant leurs scores finaux, ou en utilisant les prédictions de l'un comme input pour l'autre.

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :** Plusieurs stratégies de conception (selon la taxonomie de Burke) :
  * **Pondéré (Weighted) :** $Score_{final} = \alpha \times Score_{CF} + (1-\alpha) \times Score_{CB}$
  * **Commutation (Switching) :** Si l'item est nouveau, utiliser CB. S'il a plus de 50 notes, utiliser CF.
  * **Cascade :** CF présélectionne le Top 100, puis CB les classe plus finement en fonction des attributs.
  * **Feature Augmentation :** CB génère de nouvelles caractéristiques (features) qui sont ensuite injectées dans un modèle CF.

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Toutes les données requises par les sous-modèles : Matrice d'interactions (ratings/clics) ET métadonnées/textes des items/utilisateurs.

### 4. Avantages (Pros) 👍
* **Surmonte le Cold-Start :** Le problème majeur du filtrage collaboratif est résolu grâce à l'apport du filtrage par contenu.
* **Précision maximale :** En général, les modèles hybrides battent toujours les modèles simples car ils exploitent plus de signaux de données.
* Très robuste et adaptable en production.

### 5. Inconvénients et Limites (Cons) 👎
* **Complexité d'ingénierie :** Beaucoup plus dur à implémenter, à maintenir et à débugger.
* **Coût de calcul (Compute) :** Nécessite de faire tourner plusieurs algorithmes en parallèle (ou en série).
* **Réglage des hyperparamètres :** Trouver le bon ratio de pondération ($\alpha$) entre les différents modèles est complexe.

### 6. Métriques d'évaluation pertinentes
* Identiques aux modèles simples : RMSE, NDCG, Precision@K. On s'attend à une amélioration globale sur toutes ces métriques par rapport aux modèles isolés.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement vs Inférence :** Lourds. Les systèmes en cascade peuvent optimiser l'inférence (le premier filtre rapide réduit le nombre d'items avant de passer au modèle complexe).
* **Complexité :** L'architecture système devient le vrai défi (orchestration de micro-services souvent nécessaire).

### 8. Cas d'usage Typiques & Exemples réels
* **Netflix :** Combine le filtrage collaboratif (historique des utilisateurs) avec du filtrage basé sur le contenu (acteurs, réalisateurs, genres) et des méthodes de deep learning.

### 9. Bibliothèques et Outils (Implémentation)
* `LightFM` (Excellente librairie Python qui implémente un hybride Factorisation de Matrice + Content-based).
* `TensorFlow Recommenders` (TFRS permet de créer facilement des architectures hybrides complexes avec des réseaux de neurones).
