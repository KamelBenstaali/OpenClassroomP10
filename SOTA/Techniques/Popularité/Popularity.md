# Algorithme de Recommandation : Popularité Avancée (Time Decay)

### 1. Principe de base (L'intuition)
* **Description en une phrase :** Recommander à tous les utilisateurs les articles du moment qui ont attiré le plus de lecteurs uniques, tout en pénalisant le score des articles trop vieux.
* **Comment ça marche ?** Au lieu de simplement compter le nombre total de clics (ce qui avantagerait éternellement les vieux articles ou les clics frénétiques d'un seul utilisateur), on compte combien de personnes différentes ont lu l'article, et on divise ce score par l'âge de l'article. Ainsi, un article très récent a besoin de beaucoup moins de lecteurs pour passer en tête des recommandations.

### 2. Fonctionnement Mathématique / Algorithmique
* **La mécanique sous-jacente :**
  Nous avons conçu une formule personnalisée "Time Decay" (Amortissement temporel) :
  $$ Score\_Popularite = \frac{Nombre\_Utilisateurs\_Uniques}{Age\_en\_Heures} $$
  * **$Nombre\_Utilisateurs\_Uniques$ :** Évite l'inflation artificielle des scores par un seul utilisateur obsessionnel ou par un bug (Click Farming). Mesure le véritable attrait global.
  * **$Age\_en\_Heures$ :** Calculé comme la différence temporelle entre le "Présent" (la date de l'article le plus récent du jeu de données) et la date de publication de l'article évalué. On y ajoute mathématiquement $+1$ pour éviter une division par zéro sur un article fraîchement publié.

### 3. Données requises (Inputs)
* **Quelles sont les données nécessaires au fonctionnement ?**
  * Historique d'interactions (Logs) pour compter de manière unique le couple `user_id` / `article_id`.
  * Métadonnées des articles incluant obligatoirement la **date de publication** (timestamp).

### 4. Avantages (Pros) 👍
* **Solution ultime au Cold-Start Utilisateur :** Lorsqu'un nouvel utilisateur arrive sur la plateforme sans aucun historique de lecture, c'est le seul algorithme capable de lui fournir instantanément une recommandation pertinente (les "Trending Topics").
* **Mise en avant de la "Fraîcheur" :** Dans l'industrie de la presse (News Portal), la nouveauté est souvent plus importante que la pertinence thématique stricte. Le Time Decay garantit cette fraîcheur.
* **Complexité quasi-nulle à l'inférence :** Le classement est pré-calculé globalement. Lors d'une requête API en production sur Azure, il suffit de renvoyer les 5 premières lignes du classement. Le temps de réponse est infime (proche de 0 ms).

### 5. Inconvénients et Limites (Cons) 👎
* **Zéro Personnalisation :** L'algorithme propose strictement les 5 mêmes articles à un passionné de sport et à un passionné de politique.
* **Effet "Le riche devient plus riche" (Matthew Effect) :** Les articles populaires sont affichés en tête par défaut, donc ils reçoivent mécaniquement encore plus de clics, ce qui les rend encore plus populaires au détriment des articles de niche (qui disparaissent dans la Long Tail).

### 6. Métriques d'évaluation pertinentes
* L'algorithme de popularité sert avant tout de **Baseline (Modèle de base)** lors des évaluations globales.
* Ses performances au test du *Hit Ratio@K* ou *NDCG* sont souvent très basses sur des utilisateurs fidèles par rapport à un ALS, mais il sert de point de comparaison "plancher" indispensable pour prouver l'efficacité de nos modèles d'Intelligence Artificielle.

### 7. Scalabilité et Coût de calcul (Performance)
* **Entraînement :** Très rapide (un simple groupby et quelques calculs mathématiques basiques sur des colonnes).
* **Inférence :** Immédiate.
* **Scalabilité :** Parfaite. L'algorithme résiste sans aucun problème à des millions d'interactions.

### 8. Cas d'usage Typiques & Exemples réels
* Page d'accueil par défaut de YouTube ("Tendances").
* Section "Articles les plus lus" sur les sites de presse en ligne (Le Monde, Le Figaro).
* **Fallback System :** Sert de système de secours de tout bon système de recommandation mondial lorsqu'un modèle IA complexe échoue ou crash.

### 9. Bibliothèques et Outils (Implémentation)
* Aucune bibliothèque de Machine Learning complexe (comme scikit-learn ou implicit) n'est requise.
* Une implémentation en `pandas` (Python) ou via des requêtes `SQL` (`COUNT(DISTINCT user_id)`) suffit amplement.
