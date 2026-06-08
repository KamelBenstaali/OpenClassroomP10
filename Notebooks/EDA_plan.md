
## Sur le fichier `clicks_sample.csv` (interactions)

- Dimensions du dataset (shape) et liste des colonnes de `clicks_df`.
- Période couverte par les clics via conversion de `click_timestamp` en datetime (du 1er au 3 octobre 2017, soit ~47h35min).
- Nombre d’utilisateurs uniques, nombre d’articles uniques cliqués et nombre total d’interactions.
- Nombre moyen d’interactions par utilisateur (2.66 interactions/user).
- Distribution du nombre d’interactions par utilisateur (min, médiane, moyenne, max).
- Visualisation 1 : histogramme du nombre d’interactions par utilisateur + boxplot associé.
- Visualisation 2 : top 15 des articles les plus cliqués (barplot), avec affichage détaillé du top 5 et annotation du nombre de clics sur les barres. 
- Note explicite sur la courte durée temporelle (47h35min) rendant les patterns temporels peu exploitables. 

## Sur `articles_metadata.csv` (métadonnées articles)

- Dimensions du dataset et liste des colonnes de `articles_df`. 
- Visualisation 3 (analyse des métadonnées) comprenant  : 
  - Distribution du top 10 des catégories d’articles (`category_id`).  
  - Distribution du nombre de mots par article (`words_count`) avec binning par tranches (paramétrage par percentile 99, taille de bin, etc.) et indication du 99ème percentile.  
  - Distribution du top 10 des éditeurs (`publisher_id`).  
  - Extraction de l’année de publication à partir de `created_at_ts` et courbe du nombre d’articles publiés par année (historique 2006–2018).  
- Statistiques de synthèse sur les métadonnées :  
  - Nombre de catégories uniques.  
  - Nombre d’éditeurs uniques.  
  - Nombre de mots médian par article.  
  - Période de publication min–max (années).

## Matrice user–item et sparsité

- Construction d’une matrice user–article à partir de `clicks_df` (groupby user_id, click_article_id).
- Calcul des métriques de sparsité sur la matrice complète : taille (707 × 323), nombre de cellules totales, nombre de cellules non nulles et pourcentage de sparsité (~99.18%).
- Visualisation 4 :  
  - Heatmap user–article sur un échantillon 50 × 50 (50 users × 50 articles les plus populaires).
  - Diagramme en secteurs (pie chart) montrant proportion de cellules non nulles vs nulles, avec indication de la sparsité.
- Explication textuelle de la notion de sparsité dans les systèmes de recommandation et lien avec la difficulté du collaborative filtering et l’intérêt d’une approche content-based.

## Alignement des données et embeddings

- Comparaison du nombre d’articles dans `articles_df` et dans la matrice d’embeddings (`embeddings.shape[0]`).
- Vérification du range des `article_id` (min = 0, max = 364046) et confirmation de l’alignement `article_id` ↔ index des embeddings.
- Analyse spécifique des embeddings pour le content-based :  
  - Shape des embeddings (364047 × 250).  
  - Type (float32) et taille mémoire (~347.2 MB).  
  - Qualité : nombre de valeurs nulles, infinies, et range des valeurs min–max.

## Préparation des structures pour les modèles (partie “analyse pour modélisation”)

Même si c’est déjà orienté modélisation, il y a une mini‑EDA structurante :

- Construction du dictionnaire `user_articles_dict` (user_id → liste des articles cliqués) et statistiques sur “nombre d’articles cliqués par utilisateur” (min, médiane, moyenne, max).
- Construction de la matrice user–item pour le collaborative filtering via `analyze_for_collaborative` avec recalcul de la sparsité et distribution des “ratings” implicites (nb de clics : min, médiane, moyenne, max, qui sont tous à 1).