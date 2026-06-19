# État de l'Art : Les Systèmes de Recommandation

Les systèmes de recommandation sont des algorithmes visant à suggérer des éléments pertinents (articles, films, produits) aux utilisateurs en fonction de leurs préférences explicites ou implicites. 

Ce document résume les principales techniques existantes (State of the Art - SOTA) qui seront implémentées et comparées dans notre projet "My Content" sur **l'intégralité de la base utilisateurs**.

---

## 0. L'Approche Basée sur la Popularité (Baseline)
C'est la méthode la plus basique mais souvent indispensable. Elle consiste à recommander à tout le monde les articles les plus lus du moment.
- **Formule classique :** Comptage pur du nombre de clics ou du nombre d'utilisateurs uniques par article.
- **Formule avancée (Time Decay) :** On divise le score de clics par l'ancienneté de l'article (son âge) pour favoriser la nouveauté (un aspect critique dans le domaine de la presse).
- **✅ Avantages :** Extrêmement rapide, résout instantanément le problème du démarrage à froid (Cold Start) pour les nouveaux utilisateurs.
- **❌ Inconvénients :** Aucune personnalisation. Recommande strictement la même chose à tout le monde.

---

## 1. L'Approche Basée sur le Contenu (Content-Based Filtering)

L'approche basée sur le contenu s'appuie sur les **caractéristiques des éléments (items)** et le profil de l'utilisateur. Le principe fondamental est : *"Recommander des articles similaires à ceux que l'utilisateur a aimés ou consultés par le passé."*

### Techniques que nous allons tester :
- **Similarité Cosinus :** Mesure l'angle entre deux vecteurs (embeddings ACP) d'articles. C'est la référence pour l'analyse de textes.
- **Distance Euclidienne :** Mesure la distance spatiale "à vol d'oiseau" entre deux vecteurs. Nous la comparerons à la similarité Cosinus pour voir si elle offre un meilleur temps de calcul ou une meilleure précision.

### ✅ Avantages :
- Pas de Cold Start pour les nouveaux articles : Dès qu'un nouvel article est publié, ses métadonnées ou embeddings permettent de le recommander.
- Transparence et indépendance vis-à-vis du comportement des autres utilisateurs.

### ❌ Inconvénients :
- **Bulle de filtres :** Manque de "sérendipité" (tendance à enfermer l'utilisateur dans les thématiques qu'il connaît déjà).
- Cold Start pour les nouveaux utilisateurs (aucun historique sur lequel se baser).

---

## 2. Le Filtrage Collaboratif (Collaborative Filtering)

Le filtrage collaboratif repose uniquement sur les **interactions passées (clics, temps de lecture)**, sans chercher à comprendre le contenu des articles. Principe : *"Si deux utilisateurs ont eu le même comportement par le passé, ils auront probablement les mêmes goûts à l'avenir."*

### Techniques que nous allons tester :
**A. Memory-Based (KNN Users)**
Utilise l'algorithme des K-plus proches voisins (K-Nearest Neighbors) directement sur la matrice pour trouver les utilisateurs qui te ressemblent mathématiquement, et te recommander ce qu'ils ont lu.
- **Inconvénient :** Très coûteux en mémoire et en latence d'inférence sur de larges datasets.

**B. Model-Based (SVD et ALS)**
Au lieu de calculer des distances directes à chaque requête, ces méthodes construisent un modèle mathématique abstrait (factorisation de matrices).
- **SVD (Singular Value Decomposition) :** Modèle classique très performant, mais historiquement pensé pour des notes explicites (ex: 5 étoiles). Nous devrons simuler un score d'appréciation via un *preprocessing* pour l'utiliser avec de simples clics.
- **ALS (Alternating Least Squares) :** Modèle massivement optimisé pour les données **implicites** (comme nos historiques de clics).

### ✅ Avantages :
- **Sérendipité :** Permet des découvertes transversales inattendues grâce à l'intelligence collective (si les autres ont aimé, tu aimeras peut-être).
- Pas besoin d'analyser ou de stocker le texte des articles.

### ❌ Inconvénients :
- Problème de la matrice creuse (Sparsity) et Cold Start complet pour les nouveaux articles non cliqués et les nouveaux utilisateurs.

---

## 3. Les Approches Hybrides

Pour pallier les défauts respectifs du Content-Based (Bulle de filtre) et du Collaborative Filtering (Cold start), les systèmes modernes combinent plusieurs techniques.

### Technique que nous allons tester :
- **Borda Count (Hybride Pondéré) :** Nous générerons des listes de recommandations avec nos différents modèles (ex: ALS + Content-Based + Popularité) et nous attribuerons des points pondérés (ex: 40% ALS / 40% Contenu / 20% Pop) à chaque article selon sa position dans les classements. L'article avec le meilleur score combiné final est recommandé.

---

## 🎯 Conclusion & Stratégie de Benchmark

Dans notre projet MVP, **tous les algorithmes décrits ci-dessus seront soumis à un Benchmark sur l'intégralité des utilisateurs de la base de données**. 

Nous utiliserons un jeu de Train/Test rigoureux (méthode du *Leave-One-Out* chronologique) pour éviter la fuite de données, et nous mesurerons :
1. **Les performances métiers :** Hit Ratio@5, MRR (Mean Reciprocal Rank), Couverture du catalogue (Coverage).
2. **Les performances techniques (critiques pour Azure Functions) :** Temps de réponse (Latence), Taille de la RAM consommée par les fichiers prérequis (matrices, embeddings).

Le modèle (ou le système hybride) offrant le meilleur compromis Pertinence / Latence sera sélectionné pour le déploiement.
