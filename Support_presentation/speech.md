# 🎤 Script Détaillé de Soutenance : GloboNews

Ce document contient l'organisation de ta présentation slide par slide.
Pour chaque slide, tu trouveras ce que tu dois **écrire sur la présentation** (très synthétique) et ce que tu dois **dire à l'oral** (ton discours).

--

## Plan de présentation
- Contexte & Mission
- Jeu de données
  - Présentation des differents types de fichiers
  - Aborder la structure des fichiers des cliques et des articles
  - Présenter des analyses EDA
- Modélisations
  - Approche d'évaluation et métriques.
  - benchmark des approches Filtrage collaboratif
    - presentation des differents models
    - performances
    - choix retenu
  - benchmark des approches Approche sémantique
    - presentation des differents models
    - performances
    - choix retenu
  - Popularité (comment le scoring popularité est mis en place)
  - L'Hybridation et les Leçons Apprises
    - Comment les coefficients des approches ont été choisies
    - performances
- Architecture Technique & Démonstration (MVP)
  - Back-End : API Serverless (Azure Functions) -> Scalabilité & Coûts réduits.
  - Front-End : Application Streamlit moderne.
  - Résilience : Système de Fallback intégré en cas de panne de l'API.
  - *(Insérer le Schéma de l'Architecture Retenue)*
  - *(Capture d'écran / Démo de l'app)*
- Architecture Cible & Perspectives (Passage à l'échelle)
  - Séparation du Code et de la Donnée (MLOps).
  - CI/CD pour le code et automatisation du ré-entraînement (Azure Data Factory).
  - Évolutions : Recommandation Temps Réel (Kafka) et Features contextuelles.

- Conclusion

##################################################@@@





## Dernière Slide : Conclusion

**Contenu affiché sur la Slide :**
* Objectif atteint : Moteur hybride supérieur aux approches classiques, réactif et sécurisé.
* Prêt pour le déploiement Cloud.

**Speech (À dire à l'oral) :**

* Je vous remercie pour votre attention, et je suis prêt à répondre à vos questions !