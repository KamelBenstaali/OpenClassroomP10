# Plan d'Action - Projet P10 : My Content (Système de Recommandation)

Ce plan est basé sur la description de la mission et les données disponibles dans votre dossier `Data`. Le but final est de développer un MVP d'une application de recommandation d'articles basée sur une architecture serverless (Azure Functions).

## Étape 1 : Analyse Exploratoire des Données (EDA) et Préparation
Avant de construire le modèle, vous devez comprendre et préparer vos données :
- **Exploration des fichiers :**
  - `articles_metadata.csv` : Analyser les informations sur les articles (catégories, nombre de mots, dates).
  - `clicks/` (dossier) : Agréger les historiques de clics des utilisateurs pour comprendre leurs interactions et leurs préférences.
  - `articles_embeddings.pickle` : Analyser les représentations vectorielles (embeddings) des articles qui vous permettront de calculer des similarités de contenu.
- **Optimisation des données :**
  - **Réduction de dimension :** Comme suggéré par Julien, appliquez une **ACP (Analyse en Composantes Principales)** sur `articles_embeddings.pickle`. Ce fichier est volumineux (~364 Mo) et sa réduction facilitera son déploiement sur les services gratuits d'Azure.

## Étape 2 : Modélisation du Système de Recommandation
Vous devez concevoir la logique qui permettra de suggérer 5 articles pertinents :
- **Approche de Popularité :** Recommander les articles les plus lus ou les plus cliqués globalement, particulièrement utile pour les nouveaux utilisateurs (problème du "Cold Start").
- **Approche Content-Based :** Recommander des articles similaires à ceux que l'utilisateur a déjà lus en utilisant la similarité cosinus sur les embeddings réduits.
- **Approche Collaborative Filtering :** Recommander des articles basés sur le comportement d'utilisateurs similaires (en utilisant les données de clics).
- **Méthode Hybride :** Combiner les approches Content-Based et Collaborative Filtering pour tirer parti des avantages de chacune.
- **Sélection :** Évaluer et comparer ces approches. Choisissez l'algorithme le plus adapté à intégrer dans votre MVP. L'objectif est de prendre un `user_id` et de renvoyer une liste de 5 `article_id`.

## Étape 3 : Développement et Déploiement de l'Azure Function (Serverless)
C'est le cœur technique de votre MVP. L'architecture serverless permet de faire tourner votre modèle à la demande :
- **Création de la fonction :** Développer un script Python pour Azure Functions.
- **Logique d'exécution :** La fonction doit recevoir une requête contenant un `user_id`, exécuter le système de recommandation, et retourner les 5 recommandations au format JSON.
- **Intégration du stockage :** Utilisez la fonctionnalité **“Azure Blob storage input binding”** pour charger vos données réduites (matrice d'embeddings ACP, etc.) directement dans la fonction, évitant de créer une API séparée.
- **Déploiement :** Déployer la fonction sur Azure en utilisant le plan "Consommation (serverless)" pour éviter les coûts hors utilisation. *N'oubliez pas de désactiver les ressources après vos tests.*

## Étape 4 : Développement de l'Interface Utilisateur (Application)
Créer une interface simple pour que Samia (la CEO) puisse tester le MVP :
- **Choix du Framework :** **Streamlit** est fortement recommandé car il est très rapide à mettre en place pour les applications Data. (Flask est aussi une option valide).
- **Fonctionnalités de l'app :**
  1. Une liste déroulante ou un champ texte pour sélectionner un `user_id`.
  2. Un bouton pour déclencher la recommandation.
  3. L'application envoie l'ID à l'Azure Function (via une requête HTTP).
  4. L'application affiche de manière claire les 5 articles recommandés (en utilisant les métadonnées pour afficher par exemple l'ID, la catégorie, etc.).

## Étape 5 : Industrialisation et Gestion de Version
Montrez que votre projet est structuré et prêt pour la production :
- **GitHub :** Initialisez un dépôt Git en local. Organisez votre code en dossiers clairs (ex: `notebooks/` pour l'EDA et modélisation, `azure_function/` pour le code serverless, `app/` pour le code Streamlit).
- **Documentation :** Ajoutez un `README.md` expliquant comment lancer le projet.
- **Push :** Poussez l'ensemble de votre code sur GitHub.

## Étape 6 : Préparation de la Soutenance
Préparez une présentation PowerPoint (ou format PDF, 15 à 25 slides) qui répond aux attentes de Samia :
1. **Description fonctionnelle :** À quoi sert l'application.
2. **Comparaison des modèles :** Les différentes approches de modélisation testées, leurs avantages et inconvénients.
3. **Architecture retenue (MVP) :** Un schéma montrant l'application Streamlit communiquant avec l'Azure Function, qui elle-même lit sur le Blob Storage.
4. **Architecture cible :** Un schéma expliquant comment l'architecture devra évoluer pour gérer de manière dynamique (à chaud) l'**ajout de nouveaux utilisateurs** et de **nouveaux articles** (ex: mise à jour des embeddings en temps réel, base de données NoSQL pour stocker l'historique utilisateur, etc.).

---
*Voulez-vous que l'on commence par la première étape (l'exploration des données et l'ACP sur les embeddings) ?*
