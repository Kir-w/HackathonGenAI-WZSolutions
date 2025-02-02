# HackathonGenAI-WZSolutions

La solution que nous proposons pour le use case de Veolia consiste à identifier des indicateurs clés sur la qualité des données, puis à déployer un système basé sur l'IA générative pour automatiser la détection des données de mauvaise qualité et automatiser l'amélioration de cette qualité.

Équipe : Prosper WANG, Kylie WU, Mark-Killian ZINENBERG, Ilan ZINI\
Nous sommes étudiants en Master 1 à l'ESILV (Paris). 



## Overview

**Contexte**\
Veolia Eau France dispose d'un entrepôt de données volumineux et structuré. Les données sont utilisées par 15 000 collaborateurs pour des décisions critiques liées à l'opération du service de l'eau (facturation, abonnés, compteurs, patrimoine de l’entreprise...). Il devient difficile pour les Data Engineers et Data Scientists à gérer la qualité des données à grande échelle.

**Enjeu**\
Améliorer la qualité des données pour accélérer les processus des équipes Data. Faciliter l'identification et la mise en place de contrôles de qualité sur les données à grande échelle.

**Objectif**\
Développer une solution qui utilise des méthodologies d’IA générative (agent(s) IA) pour automatiser la création et la mise à jour de contrôles qualité sur les données.

**Entrées et sorties**\
Entrée : une base de donnée qui contient les tables dont on veut évaluer la qualité.\
Sortie: une liste d'anomalies que nous avons repéré sur les tables, ainsi que les requêtes SQL qui premettent de trouver les données de mauvaises qualité dans nos tables. 

**Compléments**\
Pour automatiser ce processus décrit plus haut, nous allons créer un agent IA.\
Cet agent est au coeur de notre problème: c'est lui qui va s'appuyer sur un modèle LLM pour répondre à nos besoins.\
Il va d'abord devoir reconnaitre les tables qu'on lui donne en entrée, comprendre leur sens, leur fonctionnalité, leurs colonnes, donc deviner de quel type de données il s'agit à partir du nom des colonnes et du contenu de la base de données pour rester généraliste.\
Une fois cette identification faite, il va devoir parcourir les tables de la base de données et trouver des anomalies dans celles-ci. Il devrait répondre à la question: ces tables contiennent-elles des données de mauvaise qualité, si oui lesquelles et pourquoi ?\
Pour parvenir à cela, il sera aidé des indicateurs que nous lui donnerons et de la stratégie de prompt engineer que l'on a mis en place. 



## Notre projet, étape par étage

Voici une présentation de notre projet, étape par étape. 


### Etape 1: fichiers CSV
Cette étape, ainsi que l'étape 2, sont propres à notre projet et ne sont pas importantes ni utiles dans le projet concret de Veolia car ils travaillent directement sous forme de base de données (Google Cloud) alors que nous avons du commencer à partir de fichiers CSV. A mettre en italique. 

En effet, au début de notre Hackathon, nous avons reçu 3 fichiers CSV.  C'était notre data et nous devions partir de cela.\
Ces 3 fichiers CSV correspondaient à des échantillons des tables 'consommations', 'abonnements' et 'factures'.

La toute première étape fut d'analyser ces fichiers CSV et de convertir le type des colonnes dans le bon format: par exemple, transformer les colonnes qui contiennent des dates de type 'object' à type 'datetime'.\
Nous avons fait cela dans le notebook 'redshift.ipynb'. Ce notebook contient tout le code qui nous a permis de faire cette étape de data pre-processing. C'est également depuis ce notebook que l'on a généré nos nouveaux fichiers CSV corrigés.


### Etape 2: Redshift
La deuxième étape consistait à mettre ces fichiers CSV corrigés dans une base de données.\
Pour cela nous avons utilisé les outils Amazon à notre disposition et notamment Amazon S3 et Amazon Redshift.

Amazon S3 est une solution de stockage et Amazon Redshift est une base de données relationnelle.\ expliquer plus en détail ces 2 outils
Nous avons d'abord mis nos 3 fichiers CSV dans S3 puis nous les avons stockés dans la base de données Redshift, sous le schéma 'public'.

A partir de là, nous avions une base solide pour commencer la partie IA générative.


### Etape 3: agent IA
C'est dans cette étape que nous avons créer notre agent IA. C'est à partir de là que nous sommes entrés dans le coeur du sujet. 

Nous avons créé un agent IA capable de prompter un modèle LLM et doté de capatiés RAG pour avoir un accès direct à notre base de données Redshift. 

En effet, nous avons établi une connection avec Amazon Redshift ainsi qu'avec Amazon Bedrock.

Par ailleurs, nous avons choisi le modèle LLM Mistral AI 8x7B Instruct car il est le meilleur rapport qualité prix.\
Nous avons réalisé des tests de comparaison entre Nova Pro et Claude 3 Sonnet. Ces 2 modèles sont tous deux plus performants que Mistral, mais aussi plus coûteux. Titan G1 Express a aussi été considéré, mais ses résultats étaient insatisfaisants en termes de coût et de performance.\
Nous avons donc choisi Mistral AI 8x7B Instruct. 

Puis nous avons plusieurs prompts à notre agent afin d'avoir les meilleurs output possibles et les plus cohérents avec ce que l'on souhaite. 


### Etape 4: frontend
Nous avons essayé de relier notre backend (notre prompt et les outputs de notre agent) avec un frontend.

Nous voulions une belle inferface, user-friendly.

Pour le frontend, nous utilisons StreamLite. explique ce que c'est



## Nos difficultés

Nous avons rencontrés de nombreuses difficultés lors de la réalisation de ce Hackathon. 

Premièrement, nous avons essayé de créer notre agent et notre knwoledge base depuis la console Amazon Bedrock. C'est ce que l'on nous a conseillé et suggéré de faire. Le but était de les créer via la console Amazon puis une fois crééent, de les appeler dans notre code principal (VS code).\ 
Seulement, nous sommes arrivés presqu'au bout mais pas au bout. Ca ne marchait pas à la fin et nous avions fait tout ca pour rien car nous avons complétement abandonné l'idée.\
C'était une très mauvaise idée également car nous avons passé énormément de temps à regarder des tutos pour comprendre comment la console marchait et énormement de temps à régler des problèmes car rien ne marchait. Nous avions des problèmes de permissions, ce qui n'était même pas de notre faute mais qui nous a bloqué pendant trop longtemps.\
Au bout d'un moment, nous avons décidé d'abandonner et d'opter pour une autre méthode: créer l'agent et la knowledge base nous meme via VS code et non la console Amazon Bedrock. 

Une autre difficulté fût la connection à Amazon Redshit (la base de données) depuis VS code.\
Nous n'arrivions pas à l'établir donc nous avons décidé de créer notre agent à partir de la plateforme de stockage Amazon S3 et non la base de données Redshift.\
Nous avons réussi et nous avons poussé ce processus loin. Seulement, travaillant en parallèle sur la connection avec Redshit, un autre membre du groupe a finalement réussi à l'établir, ce qui nous as fait délaissé notre travail sur Amazon S3. On peut donc considérer cela comme une perte de temps. 

Enfin, nous avons recontré des difficultés quant à la partie prompt engineering. En effet, nous avons essayé d'établir une vraie stratégie de prompt engineering pour que notre agent soit le plus performant possible. Nous nous sommes énormement cresé la tête sur cette partie qui fût probablement la plus importante.\
La difficulté résidait également dans le manque de temps que l'on avait pour cette partie car nous avions perdu trop de temps auparavant sur la partie technique de l'implémentation de l'agent, comme décrit ci-dessus. 



## Point forts

Nous avons énormément communiqué et fait de points (réunions) pour ne pas s'égarer et être certain que tout le monde prenait la même direction. 

Nous ne sommes pas restés bloqué trop longtemps sur le meme probleme. Nous avons régulièrement opté pour explorer d'autres options et nous n'avons pas hésité à changer de direction si nous n'allions pas dans la bonne. 

donne moi en 2 autres. 



## Pour aller plus loin 

- multi-agents
- plannification: faire des analyses périodiques avec Lambda ou AWS Step Functions 
- intégration de l'agent dans un Pipeline CI/CD 

explique et détail les 3 points