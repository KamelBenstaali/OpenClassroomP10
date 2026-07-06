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
- `test_api.py` : Tests d'intégration automatisés de la réponse HTTP de l'API.
- `test_blob.py` : Tests d'infrastructure validant la connexion et l'intégrité du stockage Azure Blob.

## Tests et CI/CD
L'API est couverte par des tests unitaires et d'intégration utilisant le framework **Pytest**.
Ces tests vérifient :
- Que la connexion au Cloud Blob Storage fonctionne et que les 5 fichiers critiques sont présents (`test_blob.py`).
- Que l'API répond avec le bon code HTTP, gère le Cold-Start correctement, et formate parfaitement son JSON (`test_api.py`).

**Exécuter les tests en local :**
Pour exécuter les tests depuis votre machine, placez-vous dans le dossier `AzureAPI` et lancez :
```bash
pip install pytest requests azure-storage-blob
pytest .
```
*(Note : Le test du Blob sera automatiquement ignoré (Skipped) si la variable `AZURE_STORAGE_CONNECTION_STRING` n'est pas définie dans votre environnement, pour éviter les erreurs lors des développements hors-ligne).*

**Intégration Continue (GitHub Actions) :**
Ces tests sont intégrés dans le pipeline de déploiement continu (`.github/workflows/azure-functions-app-python.yml`). À chaque modification du dossier `AzureAPI` poussée sur la branche `main`, un serveur Ubuntu télécharge les dépendances et exécute ces tests. 
Le déploiement vers la production sur Azure n'a lieu que si 100% des tests réussissent, garantissant la fiabilité de l'API.
