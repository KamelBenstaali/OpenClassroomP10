Voici la feuille de route exacte pour construire l'Azure Function. C'est un mini-projet en soi, qui se déroule en 4 étapes :

### Étape 1 : Initialiser le projet Azure Functions (en local)
Créer un nouveau dossier sur l'ordinateur (hors des notebooks) dédié à l'API.

**Commandes Terminal :**
```bash
# 1. Se placer dans le dossier du projet
cd /Users/kamelbest/Documents/Openclassroom_projets/P10

# 2. Créer le dossier pour l'API et s'y déplacer
mkdir AzureAPI
cd AzureAPI

# 3. Initialiser le projet Azure Function (Modèle Python V2)
func init --worker-runtime python --model V2

# 4. Créer la fonction HTTP (La route web)
func new --name recommend --template "HTTP trigger" --authlevel "anonymous"
```

*Le fichier `requirements.txt` a été généré, il suffit de l'éditer avec les packages nécessaires (numpy, pandas, scipy, implicit, scikit-learn, pyarrow).*

### Étape 2 : Préparer les cerveaux (Les Artefacts)
Regrouper tous les fichiers générés par les modèles au même endroit.

**Commandes Terminal :**
```bash
# 1. Créer le dossier data/ à l'intérieur de AzureAPI/
mkdir data

# 2. Copier les fichiers depuis les téléchargements Google Drive vers data/
# (S'assurer d'avoir téléchargé "Collaborative_best" et les historiques avant)
cp ../Generated/Collaborative_best/als_user_factors.npy data/
cp ../Generated/Collaborative_best/als_item_factors.npy data/
cp ../Generated/Collaborative_best/als_user_mapping.pkl data/
cp ../Generated/Collaborative_best/als_item_mapping.pkl data/

cp ../Generated/articles_embeddings_pca.pickle data/
cp ../Generated/Popularity_data/articles_popularity_time_decay.parquet data/
cp ../Generated/user_histories_dict.pkl data/
cp ../Generated/hybrid_weights.json data/
```
*(Alternative : Si Azure refuse de déployer un fichier de 145 Mo, il faudra les stocker sur un "Azure Blob Storage" et configurer l'API pour les télécharger au démarrage. Cependant, pour un MVP, les regrouper dans un dossier `data/` est souvent suffisant).*

### Étape 3 : Coder l'API (`function_app.py`)
Éditer le script `function_app.py` généré à l'étape 1.

1. **Au démarrage global (Cold Start de l'API) :** Charger tous les fichiers `.pkl` et `.npy` en mémoire vive (RAM) dans des variables globales. Il ne faut surtout pas les charger à chaque requête client !
2. **La Route `/api/recommend` :** Créer une fonction HTTP qui reçoit un `user_id` en paramètre.
3. **Le Moteur :** Réécrire la fonction `recommend_hybrid` dans ce script.
4. **La Réponse :** Retourner les 5 IDs d'articles au format JSON.

Exemple :
```python
import azure.functions as func
import logging
import json
# Autres imports (numpy, implicit, etc.)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Cette route sera accessible via : http://localhost:7071/api/recommend
@app.route(route="recommend")
def recommend_articles(req: func.HttpRequest) -> func.HttpResponse:
    ...
```

### Étape 4 : Test en local et Déploiement sur le Cloud
Avant d'envoyer sur le cloud, vérifier que l'API fonctionne en local.

**Commandes Terminal (Test local) :**
```bash
# 1. Créer un environnement virtuel propre pour l'API
python3 -m venv .venv
source .venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Allumer le serveur local Azure Functions
func start
```
*Une fois allumé, ouvrir le navigateur sur `http://localhost:7071/api/recommend?user_id=0`.*

**Commandes Terminal (Déploiement final sur Azure) :**
```bash
# 1. Se connecter au compte Azure depuis le terminal
az login

# 2. Créer une Function App sur Azure (Si ce n'est pas fait sur le portail web)
# az functionapp create --resource-group MonGroupe --consumption-plan-location westeurope --runtime python --runtime-version 3.11 --functions-version 4 --name MonApiGloboNews --storage-account MonStorageAccount

# 3. Pousser (déployer) le code local vers les serveurs de Microsoft Azure
func azure functionapp publish MonApiGloboNews
```
*L'URL retournée par la console est l'URL de production finale !*
