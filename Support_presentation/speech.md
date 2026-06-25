# 🎤 Script Détaillé de Soutenance : GloboNews

Ce document contient le discours "mot pour mot" (ou presque) que tu peux utiliser lors de ta soutenance, réparti slide par slide.

---

## Slide 1 : Introduction & Contexte (Titre)
**Ce qu'il faut dire :**
> "Bonjour à tous. Je suis ravi de vous présenter aujourd'hui le résultat de mon travail pour GloboNews. 
> Comme vous le savez, GloboNews est un acteur majeur de l'actualité en ligne. Mais aujourd'hui, le défi des médias n'est plus seulement de produire du contenu, c'est de capter et de conserver l'attention des lecteurs face à ce qu'on appelle l'infobésité. 
> Si un lecteur arrive sur notre portail et ne trouve pas immédiatement un article qui l'intéresse, il part. Mon objectif pour cette mission était donc clair : concevoir un Moteur de Recommandation (MVP) capable de suggérer en temps réel les 5 articles les plus pertinents pour chaque utilisateur."

---

## Slide 2 : Exploration des Données (EDA)
**Ce qu'il faut dire :**
> "Pour construire ce moteur, j'ai d'abord analysé notre matière première : les historiques de clics et les métadonnées des articles.
> Le premier grand enseignement de mon analyse exploratoire, c'est la confirmation d'une loi de Pareto très forte : une infime minorité d'articles monopolise la grande majorité des lectures. Cela signifie que la 'popularité' joue un rôle énorme.
> Ensuite, pour comprendre le 'sujet' des articles, j'ai utilisé les embeddings fournis. Cependant, manipuler des matrices de 250 dimensions ralentissait énormément les calculs. J'ai donc appliqué une réduction de dimension via une ACP (Analyse en Composantes Principales) pour compresser l'ADN mathématique de nos articles en 50 dimensions, ce qui a accéléré les temps de calcul de manière drastique sans perdre la sémantique de base."

---

## Slide 3 : L'Architecture Modulaire (Les 3 Cerveaux)
**Ce qu'il faut dire :**
> "Plutôt que de tout miser sur un seul algorithme, j'ai pris la décision d'architecture de construire un moteur modulaire composé de trois 'cerveaux' complémentaires.
> 
> Le premier cerveau, c'est l'**ALS (Filtrage Collaboratif)**. C'est notre champion des habitudes. Il repère les schémas complexes du type 'Les utilisateurs qui ont lu A ont aussi lu B'. Il est extrêmement performant pour nos utilisateurs fidèles, qu'on appelle les 'Warm Users'. Mais il a un défaut : le Cold-Start. Il est aveugle face aux nouveaux articles.
> 
> Le deuxième cerveau, c'est le **Content-Based (Similarité Cosinus)**. Il est purement sémantique. C'est lui qui sauve nos nouveaux articles : si un article vient de sortir mais qu'il parle d'IA, il le recommandera à nos amateurs d'IA en se basant sur le dernier article qu'ils ont lu.
> 
> Enfin, le troisième cerveau, c'est la **Popularité avec un facteur de déclin temporel (Time Decay)**. C'est notre filet de sécurité. Si un tout nouvel utilisateur arrive sur le site, sans aucun historique, on lui proposera simplement ce qui fait le buzz en ce moment."

---

## Slide 4 : L'Hybridation et les Leçons Apprises
**Ce qu'il faut dire :**
> "L'idée finale était de fusionner ces trois signaux.
> 
> Mais la Data Science est pleine de pièges, et j'ai rencontré un cas d'école très intéressant pendant la construction de mon script d'évaluation : le *Reverse Data-Leakage*. 
> Lors de mes premiers tests, j'avais obtenu un Hit Ratio de 0.00 % ! Après investigation, j'ai réalisé que pour empêcher le modèle de recommander des articles déjà lus, je lui passais l'historique complet de l'utilisateur... qui contenait l'article cible qu'il devait deviner ! J'avais littéralement ordonné à l'algorithme d'exclure la bonne réponse. Cela m'a rappelé l'importance d'une séparation Leave-One-Out absolument stricte.
> 
> Une fois ce bug corrigé, je voulais pondérer mes 3 cerveaux de manière scientifique. Plutôt que de choisir des poids au hasard, j'ai développé une boucle d'optimisation bayésienne avec **Optuna**. Optuna a trouvé la combinaison parfaite *(Tu pourras citer ici tes 3 chiffres exacts)* qui maximise le Hit Ratio global."

---

## Slide 5 : Déploiement et Interface (Démo)
**Ce qu'il faut dire :**
> "Un modèle n'a de valeur que s'il est utilisable. J'ai donc packagé notre moteur hybride sous forme d'une API Serverless en utilisant **Azure Functions**. Ce choix permet d'avoir une infrastructure qui 'scale' automatiquement en fonction du trafic de GloboNews, tout en minimisant les coûts.
> 
> Et pour que vous puissiez visualiser le résultat, j'ai développé une interface moderne avec Streamlit. *(Montrer une capture d'écran ou faire la démo)*. 
> Une fonctionnalité clé de cette interface est sa résilience : si l'API vient à tomber en panne, l'interface le détecte et bascule intelligemment sur un plan de secours (Fallback) en affichant les articles tendances pré-calculés. L'utilisateur n'est donc jamais face à un écran vide."

---

## Slide 6 : Conclusion & Perspectives
**Ce qu'il faut dire :**
> "En conclusion, l'objectif du MVP est atteint. Le modèle hybride tire parti du meilleur des mondes : la précision du collaboratif, la réactivité du sémantique, et la sécurité de la popularité.
> 
> Pour aller plus loin, les prochaines étapes seraient d'intégrer des features temporelles (par exemple, vérifier si l'utilisateur lit des sujets différents le matin et le soir). 
> Il faudrait également passer d'une API REST classique à une architecture orientée événements (avec Kafka par exemple), pour que le profil de l'utilisateur se mette à jour en temps réel dès sa première seconde de navigation.
> 
> Je vous remercie pour votre attention et je suis prêt à répondre à vos questions."
