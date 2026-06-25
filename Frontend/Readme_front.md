# GloboNews - Frontend (Streamlit)

Ce répertoire contient le code source de l'interface utilisateur de notre MVP, permettant de tester le moteur de recommandation de GloboNews.

## Fonctionnement
L'interface est construite avec **Streamlit**, un framework Python idéal pour déployer rapidement des dashboards interactifs liés à la Data Science.

L'application agit comme un "client" qui interroge l'API Serverless (Azure Functions) :
1. L'utilisateur sélectionne un profil de test via le menu déroulant (Lecteur fidèle, lecteur occasionnel, ou totalement inconnu).
2. L'interface envoie une requête HTTP `GET` à l'API Azure en lui passant l'identifiant utilisateur (`user_id`).
3. Elle récupère le flux JSON contenant le Top 5 des articles recommandés et leur score mathématique exact (calculé par l'algorithme hybride).
4. Elle affiche ces résultats sous forme de "cartes" d'articles avec un design UI modernisé et dynamique (CSS Custom).

## Sécurité et Fallback
Si l'API Azure vient à tomber en panne ou est inaccessible, le frontend intègre une stratégie de "Fallback" (secours) autonome. Il interceptera l'erreur réseau et affichera automatiquement une liste prédéfinie des 5 articles les plus populaires et récents du moment, garantissant ainsi qu'il n'y ait jamais d'écran vide pour le lecteur final.

## Usage Local
1. Assurez-vous d'avoir installé les dépendances, en particulier `streamlit` et `requests`.
2. Vérifiez que votre API Azure tourne bien (sur le port 7071) pour avoir de vraies données.
3. Lancez le serveur web localement :
   ```bash
   streamlit run streamlit_app.py
   ```
4. Votre navigateur s'ouvrira automatiquement sur `http://localhost:8501`.

## Déploiement
Le déploiement de cette application peut être effectué facilement en quelques minutes sur le service gratuit **Streamlit Community Cloud** (en connectant directement le dépôt GitHub), ou sur Azure App Service.
