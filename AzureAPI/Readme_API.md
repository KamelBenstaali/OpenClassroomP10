# GloboNews - Backend API (Azure Functions)

Ce répertoire contient le code source de l'API de recommandation d'articles pour la start-up GloboNews. L'API est construite avec le framework Serverless **Azure Functions** (Python).

## Fonctionnement de l'API
L'API implémente un système de recommandation hybride robuste qui combine :
1. **Filtrage Collaboratif (ALS) :** Utilise la librairie `implicit` pour calculer la proximité entre le lecteur et les articles selon la matrice d'interactions.
2. **Recommandation par le Contenu (CB) :** Utilise la Similarité Cosinus sur une version compressée (PCA) des plongements sémantiques (Embeddings) des articles.
3. **Popularité (Time Decay) :** Un système de Fallback mathématique (Cold-Start) pour les nouveaux utilisateurs, qui propose les articles les plus cliqués avec un système d'amortissement selon l'âge de l'article.

Ces trois scores sont normalisés (`MinMaxScaler`) puis combinés à la volée avec des poids définis (optimisés via Optuna).

## Architecture & Déploiement MLOps
Pour garantir des performances optimales et faciliter la mise à jour des modèles sans re-déploiement de l'API, cette architecture utilise un **Azure Blob Storage**.
Au démarrage (Cold Start), l'API télécharge dynamiquement l'intégralité des matrices et modèles directement depuis le Cloud vers sa mémoire RAM locale.

## Configuration requise
L'API nécessite qu'une variable d'environnement `AZURE_STORAGE_CONNECTION_STRING` soit définie.
Elle pointe vers un conteneur nommé `models` qui doit contenir les 8 fichiers générés par les notebooks :
- `user_histories_dict.pkl`
- `als_user_factors.npy`
- `als_item_factors.npy`
- `als_user_mapping.pkl`
- `als_item_mapping.pkl`
- `articles_embeddings_pca.pickle`
- `articles_popularity_time_decay.parquet`
- `hybrid_weights.json`

## Structure du dossier
- `function_app.py` : Le fichier principal contenant la logique métier et le téléchargement Blob.
- `requirements.txt` : Les dépendances Python (`azure-functions`, `numpy`, `pandas`, `implicit`, `scikit-learn`, `azure-storage-blob`).
- `host.json` et `local.settings.json` : Fichiers de configuration Azure.
