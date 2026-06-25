# Méthodologie d'Évaluation des Moteurs de Recommandation (Projet 10 GloboNews)

Ce document retrace l'intégralité des procédures d'évaluation quantitatives et qualitatives mises en place pour valider les modèles algorithmiques, garantir l'absence de fuite de données (Data Leakage) et aboutir à la solution hybride optimale.

## 1. La Préparation des Données : Le "Leave-One-Out" Chronologique
Pour mesurer l'efficacité des algorithmes sans tricher, nous avons mis en place une évaluation stricte simulant les conditions réelles d'utilisation.
* **Tri Chronologique :** L'historique complet des clics a été trié par date.
* **Test Set (La cible) :** Pour chaque utilisateur, nous avons isolé et masqué son **tout dernier clic**. C'est l'article cible que le moteur devra deviner.
* **Train Set (Le passé) :** Le reste de l'historique sert à construire la matrice d'entraînement. 
* **Garantie Anti-Data Leakage :** Les modèles (SVD, ALS) ont été instanciés et entraînés *uniquement* sur le `train_set`. Ils sont donc totalement aveugles quant à la cible à deviner.

## 2. Benchmark Quantitatif (Filtrage Collaboratif)
L'évaluation a porté sur 10 000 utilisateurs du Test Set. L'objectif était de mesurer le **Hit Ratio @ 5** (la cible est-elle présente dans le Top 5 recommandé ?) et la **Latence**.

### A. L'approche SVD (Model-Based Explicit)
* **Astuce de notation :** SVD (via `scikit-surprise`) nécessitant des notes explicites (étoiles de 1 à 5), nous avons converti le retour implicite (Implicit Feedback) en calculant le nombre de "sessions uniques" où un article a été lu par un utilisateur.
* **Procédure de prédiction :** SVD n'ayant pas de fonction Top-N, le système a dû calculer un score pour *chaque article du catalogue* puis les trier, ce qui a entraîné une latence inacceptable (2.4 secondes/user).
* **Résultat :** Hit Ratio = 0.00 %. L'algorithme n'est pas conçu pour classer (Ranking) des données implicites transformées.

### B. L'approche ALS (Alternating Least Squares)
* **L'interdiction de l'historique (Découverte) :** Pour obtenir une vraie recommandation "inédite" et éviter l'effet d'Aimant Mathématique (où l'algorithme recommande ce qui a déjà été lu), les articles présents dans le `train_set` ont été bannis du Top 5 lors de la prédiction (`filter_already_liked_items=True`).
* **Résultat :** Hit Ratio = **14.39 %**. Latence ultra-faible (24 ms/user). Encombrement mémoire minimal (69 Mo contre 776 Go de crash RAM pour le KNN). L'ALS est le grand gagnant collaboratif.

## 3. L'Hybridation et l'Optimisation par Optuna
L'architecture finale repose sur l'hybridation pondérée de 3 moteurs : ALS, Content-Based (Similarité Cosinus) et Popularité (Time Decay).

* **Standardisation des scores :** Avant d'additionner les scores des trois moteurs, ces derniers sont standardisés via un `MinMaxScaler` (bornés entre 0 et 1). Cela empêche les scores illimités de l'ALS d'écraser les scores géométriques bornés du Content-Based.
* **Recherche des Coefficients :** Le framework Optuna a itéré sur 30 essais pour trouver la pondération parfaite entre les trois moteurs sur notre métrique de Hit Ratio.
* **Résultat Final :** Les poids optimaux (ALS: 74%, Content-Based: 19%, Popularité: 15%) ont permis de faire bondir le Hit Ratio à **20.50 %**.

## 4. Évaluation Qualitative (Cas d'usages concrets)
L'évaluation statistique a été complétée par un "Sanity Check" sur trois Personas (profils d'utilisateurs) spécifiques :

1. **Le "Warm User" (Lecteur régulier) :**
   * *Constat :* L'ALS, fort de son poids de 74%, dicte la majorité de la recommandation. Cela garantit une personnalisation profonde basée sur le comportement complexe de la masse.
   
2. **Le "Niche User" (Lecteur mono-thématique) :**
   * *Constat :* Pour un lecteur n'ayant lu qu'une seule catégorie, le Content-Based intervient en arbitre et ajuste les résultats de l'ALS pour forcer l'apparition d'articles sémantiquement identiques à l'historique récent (approche *Session-Based* / Dernier article lu).
   
3. **Le "Cold Start" (Nouvel Utilisateur) :**
   * *Constat :* Face à un historique vide, l'ALS et le Content-Based échouent sans erreur applicative. Le moteur de Popularité joue parfaitement son rôle de filet de sécurité en recommandant les articles les plus en vogue du moment.
