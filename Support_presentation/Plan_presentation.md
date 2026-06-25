# 🎤 Script de Soutenance : Projet GloboNews (Recommandation d'Articles)

*Durée visée : Environ 15 à 20 minutes.*

## 1. Introduction & Contexte (2 min)
* **L'entreprise :** GloboNews, un portail d'actualité qui souhaite augmenter l'engagement de ses lecteurs.
* **Le problème :** L'infobésité. Trop d'articles tue la lecture. Si on ne propose pas le bon article au bon moment, le lecteur part.
* **L'objectif :** Créer un MVP (Minimum Viable Product) d'un moteur de recommandation performant, capable de fournir un Top 5 d'articles pertinents en temps réel.

## 2. Exploration des Données (EDA) (3 min)
* Présentation rapide du jeu de données : Des millions de clics et des métadonnées d'articles.
* **L'enseignement clé :** Une loi de Pareto forte. Une minorité d'articles attire la majorité des clics.
* **Traitement du texte :** Explication rapide du passage des Embeddings fournis vers une réduction de dimension (PCA). On a compressé l'ADN mathématique de chaque article en 50 dimensions pour accélérer les calculs sans perdre l'information sémantique.

## 3. Les Trois "Cerveaux" du Moteur (5 min)
*J'ai décidé de ne pas me reposer sur un seul algorithme, mais de construire une architecture modulaire à 3 piliers.*

1. **L'ALS (Filtrage Collaboratif) : Le champion des habitudes complexes.**
   * *Principe :* Il repère que "Les utilisateurs qui ont lu A ont aussi lu B".
   * *Avantage :* Très performant sur les utilisateurs réguliers (Warm users).
   * *Inconvénient :* Le problème du Cold-Start. Incapable de recommander un article publié il y a 5 minutes (car aucun clic dessus).

2. **Le Content-Based (Cosinus) : Le spécialiste sémantique.**
   * *Principe :* Il calcule la distance mathématique entre le dernier article lu et le reste du catalogue.
   * *Rôle clé :* C'est lui qui sauve les articles "Cold-Start". Si un article vient de sortir mais qu'il parle d'IA, il le recommandera à ceux qui lisent sur l'IA.

3. **Le Modèle de Popularité (Time Decay) : Le filet de sécurité.**
   * *Principe :* Les articles les plus cliqués récemment.
   * *Rôle clé :* C'est le "Joker" pour les tout nouveaux utilisateurs qui n'ont absolument aucun historique.

## 4. L'Hybridation et l'Optimisation Optuna (5 min)
*(🔥 C'est ici qu'il faut briller !)*
* **L'idée :** Fusionner ces 3 cerveaux pour que les forces de l'un compensent les faiblesses de l'autre.
* **L'anecdote du "Reverse Data-Leakage" :** Raconter le moment où le score était de 0.00% !
  * *"Lors de la conception de mon évaluation, j'ai fourni tout l'historique de l'utilisateur au modèle pour qu'il ne recommande pas des articles déjà lus. Le problème ? L'historique contenait l'article qu'il devait deviner ! J'avais littéralement interdit au modèle de trouver la bonne réponse. Une excellente leçon sur la séparation rigoureuse entre historique d'entraînement et donnée de test (Leave-one-out)."*
* **La justification des Poids (Optuna) :** 
  * *"Je ne voulais pas choisir les coefficients de mon modèle hybride au hasard. J'ai donc développé un algorithme d'optimisation bayésienne avec **Optuna**.*
  * *(Donner ici les poids trouvés par Optuna : ex: 60% ALS, 30% Content, 10% Pop).*

## 5. Déploiement Cloud & Interface (3 min)
* **Architecture Serverless (Azure Functions) :** Le modèle n'est pas qu'un notebook, c'est une véritable API REST déployable sur le Cloud.
  * Pourquoi Azure Functions ? Scalabilité automatique, facturation à la requête, idéal pour un MVP.
* **Le Frontend (Streamlit) :** Démonstration de l'interface moderne.
  * **La résilience (Fallback) :** Montrer que si l'API tombe en panne (ou si l'utilisateur est inconnu), le Frontend bascule intelligemment sur les recommandations "Populaires" pour ne jamais frustrer l'utilisateur.

## 6. Conclusion et Perspectives (2 min)
* **Bilan :** Objectif atteint. Le modèle hybride surpasse les modèles isolés, surtout en situation de Cold-Start.
* **Next Steps :** 
  * Intégrer l'heure de la journée (A/B testing pour voir si on lit des choses différentes le matin et le soir).
  * Passer d'une API "Azure Functions" basique à une architecture "Event-Driven" avec Kafka pour mettre à jour les recommandations en temps réel à chaque clic.

---
*(Fin du Script)*
