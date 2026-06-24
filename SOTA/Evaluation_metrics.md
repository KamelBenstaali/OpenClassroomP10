# Stratégie et Métriques d'Évaluation

Pour évaluer objectivement nos modèles de recommandation d'articles (basés sur des clics / Implicit Feedback) dans la perspective d'un déploiement Cloud (Azure Functions Serverless), nous adoptons une approche à la fois **Métier** (Pertinence) et **Technique** (Performance).

---

## 1. Métriques de Pertinence (Qualité Métier)
Puisque nous n'avons pas de "Notes sur 5 étoiles" à prédire, les calculs d'erreur classiques de type RMSE ne sont pas pertinents. Notre but est de mesurer la pertinence du **Classement (Ranking)**.

* **Hit Ratio @ 5 (HR@5)**
  * **Principe :** Vérifie si l'article réellement cliqué par l'utilisateur (caché dans le Test Set) est présent dans le Top 5 des recommandations proposées par l'algorithme. (Score binaire : 1 si présent, 0 sinon).
  * **Pourquoi l'utiliser ?** C'est la métrique la plus intuitive et compréhensible pour le métier.

* **Mean Reciprocal Rank (MRR)**
  * **Principe :** Calcule la moyenne de l'inverse du rang ($1/rang$) de l'article pertinent dans la liste recommandée. **Si l'article n'est pas du tout présent dans la liste, le score est de 0.**
  * **Pourquoi l'utiliser ?** Contrairement au Hit Ratio (qui vaut juste 1 ou 0), le MRR récompense fortement l'algorithme s'il place le bon article en position 1 (1 point) plutôt qu'en position 5 (0.2 point). C'est crucial car l'attention visuelle de l'utilisateur décroît extrêmement vite.

* **Couverture du Catalogue (Coverage)**
  * **Principe :** Mesure la proportion d'articles uniques du catalogue global que l'algorithme parvient à suggérer au moins une fois, sur l'ensemble de la base utilisateurs.
  * **Pourquoi l'utiliser ?** Un algorithme de pure "Popularité" aura une couverture proche de 0% (il propose toujours le même Top 5 à tout le monde), ce qui enterre 99% du catalogue de l'éditeur. On cherche un modèle capable de recommander la "Long Tail" (les articles de niche).

---

## 2. Métriques de Performance (Critiques pour le Cloud Azure)
Notre architecture cible est un MVP sur **Azure Functions** (Serverless). Dans ce contexte, certaines limites techniques sont éliminatoires.

* **Latence d'Inférence (ms)**
  * **Principe :** Le temps (en millisecondes) nécessaire au modèle pour générer une liste de recommandations pour 1 utilisateur.
  * **Objectif :** Moins de 100 à 200 ms. L'expérience utilisateur (UX) d'un portail web exige un affichage instantané. De plus, l'architecture Serverless facture généralement au temps d'exécution.

* **Empreinte Mémoire des Artefacts (RAM en Mo/Go)**
  * **Principe :** La taille combinée des fichiers requis en mémoire vive pour exécuter le modèle (Matrice de l'ALS, Embeddings PCA, Dictionnaires de Mapping).
  * **Objectif :** Rester drastiquement en dessous de la limite standard d'une Azure Function de base (généralement 1.5 Go de RAM). C'est cette métrique qui disqualifie souvent les algorithmes Memory-Based (KNN) en production.

---

## 3. Méthodologie d'Évaluation (Test)
* **Validation Chronologique (Leave-One-Out) :**
  Pour chaque utilisateur ayant au moins 2 clics dans son historique, nous utilisons tout son historique (sauf le dernier clic) pour l'entraînement. Nous isolons son **tout dernier clic chronologique** comme cible absolue à deviner (Test Set). Cela simule la réalité et évite les fuites de données du futur vers le passé.

* **Analyse par Segments d'Utilisateurs :**
  Au lieu de fournir une simple moyenne globale, les performances (HR@5) seront analysées en fonction de la maturité de l'utilisateur :
  * *Cold Start / Nouveaux lecteurs :* Utilisateurs ayant un historique très faible (ex: moins de 4 clics).
  * *Power Users :* Utilisateurs avec un historique riche (ex: plus de 15 clics).
  *Cela permet d'identifier l'expertise de chaque algorithme (ex: l'ALS brille sur les Power Users mais est en échec sur le Cold Start, nécessitant une approche Hybride).*
