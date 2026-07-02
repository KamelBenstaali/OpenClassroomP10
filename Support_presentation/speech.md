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
  - L'Hybridation et les Leçons Apprises
    - Popularité (comment le scoring popularité est mis en place)
    - Comment les coefficients des approches ont été choisies
    - performances



- Architecture Technique & Démonstration
  - Back-End : API Serverless (Azure Functions) -> Scalabilité & Coûts réduits.
  - Front-End : Application Streamlit moderne.
  - Résilience : Système de Fallback intégré en cas de panne de l'API.
  - *(Insérer le Schéma de l'Architecture Retenue)*
  - *(Capture d'écran / Démo de l'app)*


- Architecture Cible & Perspectives
  - Back-End : API Serverless (Azure Functions) -> Scalabilité & Coûts réduits.
  - Front-End : Application Streamlit moderne.
  - Résilience : Système de Fallback intégré en cas de panne de l'API.
  - *(Insérer le Schéma de l'Architecture Retenue)*
  - *(Capture d'écran / Démo de l'app)*


- Conclusion


( ce n'est pas le dernire version des slides, ce sont justes un brouillon de start seulement pour commencer à rediger le powerpoint suivant le plan de présentation ci-dessus)


## Slide 1 : Sommaire (table des matières)
- Contexte & Mission
- Jeu de données
...

---

## Slide 2 : Introduction & Contexte (Titre)

**Contenu affiché sur la Slide :**
* Projet : Conception d'un système de recommandation d'articles (MVP)
* Entreprise : GloboNews
* Objectif : Capter et conserver l'attention des lecteurs face à l'infobésité
* Solution : Suggérer en temps réel le Top 5 des articles pertinents

**Speech (À dire à l'oral) :**
* Bonjour à tous, je suis ravi de vous présenter le résultat de mon travail pour GloboNews.
* Le défi actuel des médias n'est plus seulement de produire du contenu, c'est de retenir l'attention face à la masse d'informations.
* Si un lecteur ne trouve pas immédiatement ce qui l'intéresse, il quitte le portail.
* Mon objectif pour cette mission était donc de concevoir un Moteur de Recommandation (MVP) capable de suggérer en temps réel les 5 articles les plus pertinents pour chaque utilisateur.

---

## Slide 3 : Exploration des Données (EDA) & Optimisation

**Contenu affiché sur la Slide :**
* Chiffres clés des interactions : Seulement 2.66 clics en moyenne par utilisateur.
* Sparsité extrême : La matrice Utilisateurs-Articles est vide à 99.18%.
* Loi de Pareto : Une minorité d'articles concentre la majorité des lectures (Popularité cruciale).
* Approche sémantique : Utilisation des Embeddings (ADN mathématique des articles).
* Optimisation (PCA) : Réduction de 250 à 50 dimensions.
* Résultat : Accélération drastique des calculs sans perte sémantique.

**Speech (À dire à l'oral) :**
* Pour construire ce moteur, j'ai d'abord analysé les historiques de clics et les métadonnées des articles.
* Le premier constat alarmant est le très faible nombre d'interactions : un utilisateur clique en moyenne sur seulement 2.6 articles. 
* Conséquence directe : notre matrice utilisateur-article a une sparsité de plus de 99.18% ! Nous faisons face à un énorme problème de "Cold-Start" (démarrage à froid).
* J'ai aussi remarqué la confirmation d'une loi de Pareto très forte : peu d'articles monopolisent les lectures, ce qui prouve l'importance d'utiliser un algorithme basé sur la "popularité" pour combler ce manque d'historique.
* Ensuite, pour comprendre le sujet des articles, j'ai utilisé les embeddings.
* Cependant, manipuler 250 dimensions ralentissait trop les calculs. J'ai donc appliqué une ACP pour compresser l'information en 50 dimensions.
* Cela a permis d'accélérer drastiquement l'API tout en gardant le sens des articles, nous permettant de respecter les limites de coût du Cloud.

---

## Slide 3 : L'Architecture Modulaire (Les 3 Cerveaux)

**Contenu affiché sur la Slide :**
* Moteur Modulaire : Combinaison de 3 algorithmes.
* 1. ALS (Filtrage Collaboratif) : Le champion des habitudes (Idéal pour "Warm Users").
* 2. Content-Based (Cosinus) : Approche sémantique (Gère le "Cold-Start" des nouveaux articles).
* 3. Popularité (Time Decay) : Le filet de sécurité (Pour les tout nouveaux utilisateurs).

**Speech (À dire à l'oral) :**
* Plutôt que de tout miser sur un seul algorithme, j'ai construit un moteur modulaire composé de trois "cerveaux".
* Le premier, l'ALS (Collaboratif), repère les schémas complexes ("ceux qui ont lu A lisent B"). Il est parfait pour nos utilisateurs réguliers, mais aveugle face aux nouveaux articles.
* Le deuxième, le Content-Based, est purement sémantique. Si un article vient de sortir, il le recommandera en se basant sur le dernier article lu par l'utilisateur.
* Enfin, le troisième cerveau est la Popularité avec un déclin temporel. C'est notre filet de sécurité pour proposer ce qui fait le buzz aux tout nouveaux utilisateurs sans historique.

---

## Slide 4 : L'Hybridation et les Leçons Apprises

**Contenu affiché sur la Slide :**
* Défi rencontré : Le "Reverse Data-Leakage" (Biais d'évaluation).
* Solution : Séparation Leave-One-Out stricte.
* Optimisation Scientifique : Utilisation de l'algorithme bayésien Optuna.
* Objectif : Trouver les poids parfaits pour maximiser le Hit Ratio global.

**Speech (À dire à l'oral) :**
* L'idée finale était de fusionner ces trois signaux.
* Mais j'ai rencontré un cas d'école intéressant : le "Reverse Data-Leakage". Lors des premiers tests, le modèle avait 0% de réussite car je lui ordonnais d'exclure l'article qu'il devait deviner !
* Cela m'a rappelé l'importance d'une séparation stricte de l'historique lors des tests.
* Une fois le bug corrigé, je voulais pondérer mes 3 algorithmes scientifiquement, et pas au hasard.
* J'ai donc utilisé une optimisation bayésienne avec Optuna, qui a trouvé la combinaison parfaite de coefficients pour maximiser les bonnes recommandations.

---

## Slide 5 : Architecture Technique & Démonstration

**Contenu affiché sur la Slide :**
* Back-End : API Serverless (Azure Functions) -> Scalabilité & Coûts réduits.
* Front-End : Application Streamlit moderne.
* Résilience : Système de Fallback intégré en cas de panne de l'API.
* *(Insérer le Schéma de l'Architecture Retenue)*
* *(Capture d'écran / Démo de l'app)*

**Speech (À dire à l'oral) :**
* J'ai packagé ce moteur hybride sous forme d'une API Serverless sur Azure Functions. Ce choix garantit que l'infrastructure "scale" automatiquement avec le trafic tout en minimisant les coûts.
* Pour la visualisation, j'ai développé une interface moderne avec Streamlit.
* *(Si tu montres le schéma)* : Comme vous le voyez sur ce schéma, le Front communique avec l'API, qui télécharge ses matrices directement depuis le Blob Storage au démarrage.
* Pour ce MVP, l'upload des matrices dans le Blob Storage a été fait manuellement après l'entraînement sur ma machine.
* Une fonctionnalité clé de l'interface est sa résilience : si l'API tombe en panne, le Front bascule sur un plan de secours et affiche les articles tendances. L'utilisateur n'est jamais face à un écran vide.

**Comment dessiner le schéma**

💻 Boîte 1 : L'Utilisateur (Flèche vers la boîte 2)
🖥️ Boîte 2 : Front-End (Streamlit) (Hébergé en local). (Flèche "Requête HTTP / JSON" vers la boîte 3)
⚙️ Boîte 3 : Back-End / API (Azure Functions) (Sur le cloud). (Flèche "Téléchargement au démarrage" vers la boîte 4)
🗄️ Boîte 4 : Base de Données (Azure Blob Storage) (Contient tes fichiers .npy et .pkl).


---

## Slide 6 : Architecture Cible & Perspectives

**Contenu affiché sur la Slide :**
* Objectif atteint : Moteur hybride précis, réactif et sécurisé.
* Passage à l'échelle *(Insérer le Schéma de l'Architecture Cible)* :
  * Automatisation de l'entraînement (Azure Data Factory).
* Perspectives d'évolution :
  * Intégration de features temporelles (Matin vs Soir).
  * Architecture orientée événements (Kafka) pour le temps réel.

**Speech (À dire à l'oral) :**
* En conclusion, l'objectif du MVP est atteint avec ce modèle hybride très complet.
* Pour le passage à l'échelle de l'entreprise, *(Pointer le schéma)* j'ai conçu une architecture cible séparant le code de la donnée.
* Côté code, une pipeline CI/CD classique (ex: GitHub Actions) mettra à jour l'API.
* Côté donnée (MLOps), nous prévoyons l'automatisation du ré-entraînement quotidien des matrices via Azure Data Factory. Cet orchestrateur lancera l'entraînement la nuit et écrasera automatiquement les anciens fichiers du Blob Storage, sans avoir besoin de toucher au code de l'API.
* Pour aller encore plus loin, nous pourrions intégrer des informations temporelles, car un utilisateur ne lit pas la même chose à 8h et à 22h.
* Enfin, passer d'une API classique à une architecture événementielle avec Kafka permettrait de mettre à jour le profil de l'utilisateur dès sa toute première seconde de navigation.
* Je vous remercie pour votre attention et je suis prêt à répondre à vos questions.


**Comment déssiner le schéma cible**

*Au centre et à droite, on garde le MVP (mais on rajoute la CI/CD logicielle) :*
📱 **Boîte 1 : Front-End (Streamlit)** ➔ ⚙️ **Boîte 2 : API Azure Functions** ➔ 🗄️ **Boîte 3 : Azure Blob Storage**
🐙 **Boîte 4 : GitHub Actions (CI/CD Code)** ➔ *(Flèche de mise à jour)* ➔ **Boîte 2 (API)**

*À gauche, on rajoute toute l'usine de ré-entraînement (La vraie nouveauté !) :*
📰 **Boîte 5 : Nouveaux Clics & Nouveaux Articles (Logs de GloboNews)** ➔ *(Flèche de collecte quotidienne)* ➔ 💾 **Boîte 6 : Data Lake / Base de Données brute**
🤖 **Boîte 7 : Azure Machine Learning / Databricks (L'usine d'entraînement qui fait tourner ton Notebook)**. *(Cette boîte lit la Boîte 6, entraîne le modèle, et envoie une flèche "Upload Automatique" vers la Boîte 3 "Blob Storage")*
⏱️ **Boîte 8 : Azure Data Factory (L'Orchestrateur)**. *(Une flèche avec une horloge "Tous les jours à 3h du matin" qui pointe vers la Boîte 7 pour la déclencher)*.




## Slide : Conclusions

- recap sur le plan d'action
- expliquer que chaque approche a ses avantages et ses inconvénients
- le choix du meilleur algorithme peut dépendre bcp des données (comme la par exemple la plus des users plus de 2 clicks et qui fait que l'ALS bcp avantagé malgrés ça on gagné legerement en perf grace à l'hybride qui est capable de gerer tous les cas)

- Notre preuve de concept prouve à qu'on est capable de passer à une echelle de production en suivant les perspectives citées.