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
Ces 3 fichiers CSV correspondaient à des échantillons des tables 'consommations', 'abonnements' et 'factures'.\

La toute première étape fut d'analyser ces fichiers CSV et de convertir le type des colonnes dans le bon format.\
Nous avons fait cela dans le notebook 'redshift.ipynb'. Ce notebook contient tout le code qui nous a permis de faire cette étape de data pre-processing. C'est également depuis ce notebook que l'on a généré nos nouveaux fichiers CSV corrigés.\


### Etape 2: Redshift
La deuxième étape consistait à mettre ces fichiers CSV corrigés dans une base de données.\
Pour cela nous avons utilisé les outils Amazon à notre disposition et notamment Amazon S3 et Amazon Redshift.\

Amazon S3 est une solution de stockage et Amazon Redshift est une base de données relationnelle.\ expliquer plus en détail ces 2 outils
Nous avons d'abord mis nos 3 fichiers CSV dans S3 puis nous les avons stockés dans la base de données Redshift, sous le schéma 'public'.\ 

A partir de là, nous avions une base solide pour commencer la partie IA générative.


### Etape 3: agent IA




## Nos difficultés




## Pour aller plus loin 







-----

Data exploration

-> conversion des dates en dataframes
-> résiliation / souscription