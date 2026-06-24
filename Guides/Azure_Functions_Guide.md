# 🚀 Guide Pratique : Azure Functions (Python V2) pour le MVP

Ce guide est spécialement conçu pour notre architecture de recommandation avec **Python V2** sur **MacOS**. Il s'appuie sur la documentation officielle de Microsoft que nous avons consultée.

## 🛠️ Prérequis
Installer **Azure Functions Core Tools** via `brew`. 
Accès à la commande `func` dans notre terminal.

---

## Étape 1 : Initialiser le projet Azure
Azure Functions V2 utilise une architecture moderne (similaire à FastAPI ou Flask) où toutes les fonctions sont définies par des décorateurs dans un seul fichier `function_app.py`.

Dans notre terminal, plaçons-nous dans le dossier où nous souhaitons créer notre API, puis lançons :
```bash
func init MonAPIRecommandation --worker-runtime python --model V2
cd MonAPIRecommandation
```

Cette commande va créer plusieurs fichiers essentiels :
* `function_app.py` : C'est ici que nous allons écrire le code Python de notre API.
* `local.settings.json` : Pour stocker nos variables d'environnement locales (ne jamais commiter ce fichier sur Git).
* `requirements.txt` : Pour lister les dépendances (`implicit`, `numpy`, `pandas`, `scikit-learn`, etc.).

---

## Étape 2 : Création de notre premier point d'entrée (Endpoint)
Ouvrons le fichier `function_app.py`. Par défaut, nous verrons une structure prête à l'emploi.

Voici un exemple de ce à quoi devrait ressembler notre code pour l'API de recommandation :

```python
import azure.functions as func
import logging
import json
# Nos imports (numpy, implicit, etc.)
# import numpy as np

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Cette route sera accessible via : http://localhost:7071/api/recommend
@app.route(route="recommend")
def recommend_articles(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Requête de recommandation reçue.')

    # 1. Récupérer l'ID de l'utilisateur envoyé dans la requête (ex: ?user_id=123)
    user_id = req.params.get('user_id')

    if not user_id:
        return func.HttpResponse(
             "Veuillez fournir un user_id dans l'URL.",
             status_code=400
        )

    try:
        user_id = int(user_id)
        # ========================================================
        # 2. METTRE ICI LA LOGIQUE DE NOTRE MOTEUR (ALS / HYBRIDE)
        # ========================================================
        # exemple fictif :
        # recs = model_als.recommend(user_id, ...)
        
        recommandations = [1234, 5678, 9101, 1121, 3141] # Remplacer par notre Top 5

        # 3. Renvoyer la réponse au format JSON
        return func.HttpResponse(
            json.dumps({"user_id": user_id, "recommendations": recommandations}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Erreur interne : {str(e)}")
        return func.HttpResponse("Erreur serveur", status_code=500)
```

---

## Étape 3 : Tester en local
Avant d'envoyer l'API sur le Cloud, il faut s'assurer qu'elle tourne bien sur notre Mac.

1. Installe les dépendances nécessaires dans notre environnement virtuel :
   ```bash
   pip install -r requirements.txt
   ```
2. Démarre le serveur local Azure :
   ```bash
   func start
   ```
3. Le terminal affichera une URL (souvent `http://localhost:7071/api/recommend`).
4. Ouvre notre navigateur et teste : `http://localhost:7071/api/recommend?user_id=42`

---

## 🚀 Étape 4 : Déploiement sur le Cloud
Une fois que notre API marche en local (et que nos matrices `.npy` se chargent bien !), nous pourrons la propulser sur Azure.
Nous aurons besoin de l'**Azure CLI** (`brew install azure-cli`), de nous connecter (`az login`), et de déployer notre code vers l'application Function que nous aurons créée sur le portail web d'Azure.
