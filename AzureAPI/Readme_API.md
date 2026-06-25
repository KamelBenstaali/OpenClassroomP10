# GloboNews - Backend API (Azure Functions)

Ce répertoire contient le code source de l'API de recommandation d'articles pour la start-up GloboNews. L'API est construite avec le framework Serverless **Azure Functions** (Python).

## Fonctionnement de l'API
L'API implémente un système de recommandation hybride robuste :
1. **Filtrage Collaboratif (ALS) :** Utilise la librairie `implicit` pour calculer la proximité entre le lecteur et les articles selon la matrice d'interactions.
2. **Recommandation par le Contenu (CB) :** Utilise la Similarité Cosinus sur une version compressée (PCA) des plongements sémantiques (Embeddings) des articles.
3. **Popularité (Time Decay) :** Un système de Fallback mathématique (Cold-Start) pour les nouveaux utilisateurs, qui propose les articles les plus cliqués avec un système d'amortissement selon l'âge de l'article.

Ces trois scores sont normalisés (`MinMaxScaler`) puis combinés à la volée avec des poids définis.

## Structure du dossier
- `function_app.py` : Le fichier principal contenant la logique métier (le point d'entrée HTTP `recommend`).
- `data/` : (Ignoré sur GitHub) Ce dossier doit contenir les modèles pré-calculés et exportés depuis les Notebooks d'entraînement (`.npy`, `.pkl`, `.pickle`, `.parquet`).
- `requirements.txt` : Les dépendances Python (`azure-functions`, `numpy`, `pandas`, `implicit`, `scikit-learn`).

## Usage Local
1. Installez les *Azure Functions Core Tools*.
2. Placez vos modèles dans le dossier `data/`.
3. Lancez le serveur localement :
   ```bash
   func start
   ```
4. Testez l'endpoint : `http://localhost:7071/api/recommend?user_id=0`

## Déploiement
Le déploiement peut s'effectuer de manière automatisée via le pipeline GitHub Actions ou manuellement via la CLI Azure :
```bash
az login
func azure functionapp publish <nom-de-votre-application>
```
