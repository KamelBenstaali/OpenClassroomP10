# Guide MLOps : Configuration du Blob Storage pour l'API Azure

Ce guide documente la mise en place de l'architecture "Cold Start" utilisant Azure Blob Storage pour alimenter l'API de recommandation de GloboNews. 
Cette approche permet de découpler totalement le code de l'API (très léger) de ses modèles de Machine Learning (très lourds), permettant ainsi de ré-entraîner les modèles sans avoir à redéployer le code.

---

## 1. Justification du Choix d'Architecture (Pour la soutenance)
La consigne suggérait l'utilisation de la fonctionnalité *Azure Blob Storage Input Binding*.
Cependant, l'Input Binding télécharge les fichiers à **chaque requête HTTP**. Pour un modèle de recommandation nécessitant l'import de 100 Mo de matrices (ALS, Embeddings), cela aurait engendré :
1. Une latence inacceptable pour l'utilisateur final (> 5 secondes par clic).
2. Un dépassement des limites de RAM allouées par la formule "Consommation (Serverless)".

**La solution implémentée :** Le téléchargement natif via le SDK `azure-storage-blob` lors du **Cold Start**. Les 100 Mo sont téléchargés une seule fois au premier réveil de l'API, puis stockés dans le cache de la RAM du serveur Azure pour répondre instantanément (en quelques millisecondes) à toutes les requêtes suivantes.

---

## 2. Explication de l'implémentation dans `function_app.py`

Le code de l'API a été spécifiquement conçu pour éviter d'écrire sur le petit disque dur virtuel de l'Azure Function, ce qui pourrait causer des goulets d'étranglement (I/O Bottlenecks). Tout est géré directement **en mémoire RAM**.

### A. Connexion au service
Au tout début du script (en dehors de la route HTTP, ce qui définit le "Cold Start"), l'API récupère la chaîne de connexion de manière sécurisée et s'identifie auprès d'Azure :
```python
CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "models"
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
```

### B. Chargement intelligent en mémoire RAM
Une fonction utilitaire est créée pour télécharger le flux de données (bytes) directement en mémoire grâce à `.readall()` :
```python
def load_blob_to_memory(blob_name):
    return container_client.download_blob(blob_name).readall()
```

### C. Décodage à la volée (Sans sauvegarde locale)
Plutôt que d'utiliser des chemins de fichiers (ex: `pd.read_parquet("fichier.parquet")`), on utilise le module `io.BytesIO` pour faire croire aux librairies Python (NumPy, Pandas, Pickle) qu'elles lisent un fichier, alors qu'elles lisent la mémoire RAM :
```python
# Exemple pour un Dictionnaire Pickle :
user_histories_dict = pickle.loads(load_blob_to_memory("user_histories_dict.pkl"))

# Exemple pour une matrice NumPy (Nécessite io.BytesIO) :
user_factors = np.load(io.BytesIO(load_blob_to_memory("als_user_factors.npy")))

# Exemple pour un fichier Parquet (Pandas) :
popularity_df = pd.read_parquet(io.BytesIO(load_blob_to_memory("articles_popularity_time_decay.parquet")))
```

Ainsi, l'API ne pèse que quelques kilo-octets. Dès qu'elle s'éteint (Scale-to-Zero), toute cette mémoire est libérée. À son prochain réveil, elle téléchargera systématiquement la toute dernière version des matrices présente sur le Blob Storage.

---

## 3. Configuration sur le Portail Azure

### A. Création du Conteneur
1. Dans le portail Azure, naviguez vers votre **Compte de stockage** (ex: `p10ba0c`).
2. Dans le menu de gauche, cliquez sur **Conteneurs d'objets blob** (Blob containers).
3. *(Si vous avez une erreur d'autorisation Entra ID, changez la méthode d'authentification en haut de la liste pour "Clé d'accès").*
4. Cliquez sur **+ Conteneur** et nommez-le très exactement : `models`.

### B. Upload des Artefacts
À l'intérieur du conteneur `models`, uploadez les 8 fichiers générés par l'entraînement :
- `als_item_factors.npy`
- `als_item_mapping.pkl`
- `als_user_factors.npy`
- `als_user_mapping.pkl`
- `articles_embeddings_pca.pickle`
- `articles_popularity_time_decay.parquet`
- `hybrid_weights.json`
- `user_histories_dict.pkl`

### C. Récupération de la Clé de Connexion
Pour que l'API puisse s'authentifier de manière sécurisée et lire ce conteneur :
1. Toujours dans le Compte de Stockage, allez dans le menu de gauche sous **Sécurité + réseau**.
2. Cliquez sur **Clés d'accès** (Access keys).
3. Cliquez sur "Afficher les clés" en haut de la page.
4. Sous *key1*, copiez la valeur de la **Chaîne de connexion** (Connection string). 

---

## 4. Lien avec l'Azure Function App

Pour que le code de l'API puisse utiliser cette clé sans qu'elle ne soit écrite "en dur" dans le code (faille de sécurité) :

### En Local (Tests)
Copiez la chaîne de connexion dans le fichier ignoré par Git nommé `local.settings.json` :
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_STORAGE_CONNECTION_STRING": "Collez-la-chaine-ici"
  }
}
```

### En Production (Cloud Azure)
1. Allez sur la page de votre **Function App**.
2. Dans le menu de gauche, allez dans **Paramètres > Variables d'environnement** (ou *Configuration*).
3. Ajoutez un nouveau paramètre d'application :
   - Nom : `AZURE_STORAGE_CONNECTION_STRING`
   - Valeur : *[Votre chaîne de connexion]*
4. Sauvegardez.