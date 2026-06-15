# État de l'Art (SOTA) - Techniques de Recommandation

Ce dossier documente les différentes approches de modélisation explorées pour le développement du système de recommandation d'articles du Projet P10 (My Content).

## Contenu du dossier

- **[Popularité](./Popularité)** : Approche de base visant à recommander les articles les plus lus ou les plus cliqués globalement. Cette méthode est particulièrement utile pour adresser le problème du "Cold Start" (lorsqu'un nouvel utilisateur n'a pas encore d'historique).
- **[1_Collaborative_Filtering](./1_Collaborative_Filtering)** (Filtrage Collaboratif) : Approche basée sur le comportement des utilisateurs. Elle recommande des articles en se basant sur les interactions et les historiques de clics d'utilisateurs similaires.
- **[2_Content_Based_Filtering](./2_Content_Based_Filtering)** (Filtrage Basé sur le Contenu) : Recommande des articles sémantiquement similaires à ceux qu'un utilisateur a déjà lus. Cette approche s'appuie sur la similarité cosinus calculée à partir des embeddings (représentations vectorielles) des articles.
- **[3_Hybrid_Systems](./3_Hybrid_Systems)** (Systèmes Hybrides) : Méthode combinant les approches de filtrage collaboratif et basé sur le contenu, permettant de tirer parti des avantages de chacune et de pallier leurs limites respectives.

## Objectif

L'objectif de cette recherche et de ces différentes techniques est d'évaluer et de comparer ces modèles. Cela permettra de sélectionner l'algorithme le plus adapté à intégrer dans le MVP (Minimum Viable Product), dont le rôle sera de prendre en entrée un `user_id` et de retourner une liste de 5 `article_id` pertinents.
