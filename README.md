# HackathonGenAI-WZSolutions

La solution que nous proposons pour le use case de Veolia consiste à identifier des indicateurs clés sur la qualité des données, puis à déployer un système basé sur l'IA générative pour automatiser la détection des données de mauvaise qualité.

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
Pour automatiser ce processus, nous avons créé un agent IA. Cet agent est au cœur de notre solution : il s'appuie sur un modèle LLM pour analyser la qualité des données.\
Il doit d'abord identifier les tables en entrée, comprendre leur structure, leur rôle et leurs colonnes, et déduire le type de données manipulées.\
Une fois cette analyse effectuée, il explore les tables à la recherche d'anomalies : les données sont-elles cohérentes, complètes et exploitables ?\
Pour cela, il utilise les indicateurs que nous avons définis et notre stratégie de prompt engineering.



## Notre projet, étape par étape

Voici une présentation de notre projet. 


### Étape 1 : fichiers CSV
*Cette étape et la suivante sont propres à notre projet et ne sont pas pertinentes pour Veolia, qui travaille directement sur une base de données Google Cloud.*

Au début du hackathon, nous avons reçu trois fichiers CSV constituant notre jeu de données.\
Ces fichiers représentent un échantillon des tables `consommations`, `abonnements` et `factures`.

Notre première étape a consisté à analyser ces fichiers et à convertir les colonnes au bon format : par exemple, transformer les dates stockées en `object` en `datetime`.\
Nous avons réalisé ce prétraitement des données dans le notebook `redshift.ipynb`, qui documente toutes les étapes de cette transformation. Nous y avons aussi généré de nouveaux fichiers CSV corrigés.


### Étape 2 : Redshift
Nous avons ensuite intégré ces fichiers dans une base de données Amazon Redshift en utilisant Amazon S3 comme intermédiaire.\
**Amazon S3** est une solution de stockage d'objets, tandis qu'**Amazon Redshift** est un entrepôt de données analytique permettant de stocker et interroger de grands volumes de données.\
Nous avons d'abord téléchargé nos fichiers dans S3, puis les avons importés dans Redshift sous le schéma `public`.\
Avec cette base solide, nous pouvions passer à la phase d'IA générative.


### Étape 3 : agent IA
Nous avons développé un agent IA capable de communiquer avec un modèle LLM et d'utiliser RAG (Retrieval-Augmented Generation) pour accéder à Redshift.\
Nous avons établi une connexion avec **Amazon Redshift** et **Amazon Bedrock**.

Nous avons choisi le modèle **Mistral AI 8x7B Instruct**, qui offre le meilleur rapport qualité-prix parmi les modèles testés (à côté de **Nova Pro**, **Claude 3 Sonnet**, et **Titan G1 Express**).

Nous avons ensuite défini plusieurs prompts stratégiques pour optimiser les réponses de notre agent.


### Étape 4 : frontend
Nous avons connecté notre backend à une interface utilisateur via **Streamlit**, une bibliothèque Python permettant de créer des applications web interactives facilement.

L'objectif était de proposer une interface intuitive et user-friendly pour interagir avec notre agent IA.



## Nos difficultés

Nous avons rencontré de nombreuses difficultés lors de la réalisation de ce Hackathon.

Premièrement, nous avons tenté de créer notre agent et notre knowledge base via la console Amazon Bedrock, comme cela nous avait été conseillé. L'idée était de les configurer depuis la console, puis de les appeler dans notre code principal sur VS Code. Toutefois, bien que nous soyons parvenus à une étape avancée, nous n'avions pas réussi à finaliser l'intégration. Après avoir passé un temps considérable à comprendre le fonctionnement de la console et à résoudre des problèmes techniques (notamment des problèmes de permissions qui ne dépendaient pas de nous), nous avons décidé d'abandonner cette approche au profit d'une intégration directe via VS Code.

Une autre difficulté fut la connexion à Amazon Redshift depuis VS Code. Initialement, nous n'arrivions pas à établir cette connexion, ce qui nous a poussés à développer une solution alternative utilisant Amazon S3 comme source de données pour notre agent IA. Nous avons poussé cette approche assez loin avant qu'un membre de l'équipe ne parvienne finalement à connecter Redshift à notre projet. Cela nous a amenés à abandonner l'approche S3, ce qui, en rétrospective, représente une perte de temps.

Enfin, l'une des difficultés majeures concernait la stratégie de prompt engineering. Nous avons dédié beaucoup de temps à concevoir des prompts efficaces pour optimiser les réponses de notre agent. Cependant, ayant déjà perdu beaucoup de temps sur l'implémentation technique de l'agent, nous avons dû travailler cette partie dans l'urgence, ce qui a ajouté une complexité supplémentaire à notre projet.



## Points forts

Nous avons beaucoup communiqué et organisé des points réguliers pour garder une cohérence de projet.

Nous avons su pivoter rapidement lorsque nous nous retrouvions bloqués sur une solution inefficace. 

Nous avons su déléguer efficacement les tâches, permettant un avancement en parallèle entre nous.



## Pour aller plus loin 

**Amélioration de l'architecture** : Intégrer un système **multi-agents** avec des spécialisations (ex. : un agent pour la détection d'anomalies, un autre pour la correction automatique).

**Automatisation des analyses** : Utiliser **AWS Lambda** ou **AWS Step Functions** pour exécuter des analyses périodiques et suivre l'évolution de la qualité des données.

**Intégration CI/CD** : Déployer l'agent IA dans un pipeline **CI/CD (Continuous Integration/Continuous Deployment)** pour faciliter les mises à jour et les tests en continu.



## Note

ou can check out some output examples in the `output` folder. 