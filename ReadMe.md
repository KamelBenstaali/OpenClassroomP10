# Projet P10 - My Content : Système de Recommandation

Bienvenue dans le dépôt du projet My Content. L'objectif de ce projet est de développer un MVP (Minimum Viable Product) d'une application de recommandation d'articles utilisant une architecture serverless (Azure Functions).

## Structure du Projet

Le projet est organisé selon l'arborescence suivante :

- **`Data/`** : Ce dossier contient les jeux de données bruts et traités nécessaires au projet (historique de clics, informations sur les articles, embeddings pré-calculés, etc.).
- **`Détails_mission/`** : Comprend la documentation concernant la mission globale, notamment le plan d'action détaillé et les spécifications attendues pour le système et l'application.
- **`Generated/`** : Dossier utilisé pour stocker les fichiers ou les modèles générés automatiquement lors des différentes étapes de traitement de données ou d'entraînement.
- **`Notebooks/`** : Contient les notebooks Jupyter utilisés pour l'Analyse Exploratoire des Données (EDA), la préparation des données (réduction de dimension via ACP), et les premières expérimentations de modélisation.
- **`SOTA/`** : *(State of the Art)* Dossier dédié à l'exploration des différentes techniques de systèmes de recommandation (Popularité, Filtrage Collaboratif, Content-Based et approches hybrides).
- **`requirements.txt`** : Liste de toutes les dépendances Python nécessaires à l'exécution de ce projet.
- **`venv/`** : Environnement virtuel Python (à ne pas inclure dans les commits Git).

## Prochaines Étapes (MVP)
1. **EDA et Modélisation** : Exploration des données et sélection de l'algorithme de recommandation optimal (cf. `Notebooks/` et `SOTA/`)

2. Implémenter les 4 techniques choisies de modélisation dans le dossier `SOTA/` qui sont:
- Collaborative filtring
- Content based filtring
- Popularity
- Hybrid