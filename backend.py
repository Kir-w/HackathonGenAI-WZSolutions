import boto3
import json
import time
import pandas as pd
from typing import List, Dict

# ---- CONFIGURATION AWS ----
AWS_REGION = "us-west-2"
MODEL_ID = "mistral.mixtral-8x7b-instruct-v0:1"

# ---- CONFIGURATION REDSHIFT ----
DATABASE = "dev"
WORKGROUP_NAME = "wz-solutions-redshift-workgroup"

# ---- INITIALISATION DES CLIENTS ----
redshift_client = boto3.client('redshift-data', region_name=AWS_REGION)
bedrock_client = boto3.client('bedrock-runtime', region_name=AWS_REGION)

# ---- FONCTIONS REDSHIFT ----
def get_redshift_tables():
    """Récupère la liste des tables disponibles dans la base de données Redshift."""
    sql_query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
    try:
        response = redshift_client.execute_statement(
            Database=DATABASE,
            WorkgroupName=WORKGROUP_NAME,
            Sql=sql_query
        )

        statement_id = response['Id']
        while True:
            status_response = redshift_client.describe_statement(Id=statement_id)
            status = status_response["Status"]
            if status in ["FINISHED", "FAILED", "ABORTED"]:
                break
            time.sleep(2)

        if status == "FINISHED":
            result_response = redshift_client.get_statement_result(Id=statement_id)
            tables = [row[0].get('stringValue', 'NULL') for row in result_response.get("Records", [])]
            return tables if tables else "Aucune table trouvée."
        else:
            return f"Erreur lors de l'exécution : {status_response.get('Error', 'Erreur inconnue')}"

    except Exception as e:
        return f"Erreur de connexion ou d'exécution : {str(e)}"
    

# ---- FONCTION POUR RÉCUPÉRER LES COLONNES D'UNE TABLE ----
def get_table_columns(table_name):
    """Récupère les colonnes et leur description d'une table Redshift."""
    sql_query = f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}';
    """
    try:
        response = redshift_client.execute_statement(
            Database=DATABASE,
            WorkgroupName=WORKGROUP_NAME,
            Sql=sql_query
        )

        statement_id = response['Id']
        while True:
            status_response = redshift_client.describe_statement(Id=statement_id)
            status = status_response["Status"]
            if status in ["FINISHED", "FAILED", "ABORTED"]:
                break
            time.sleep(2)

        if status == "FINISHED":
            result_response = redshift_client.get_statement_result(Id=statement_id)
            columns = [
                f"{row[0].get('stringValue', 'NULL')} ({row[1].get('stringValue', 'NULL')})"
                for row in result_response.get("Records", [])
            ]
            return columns if columns else "Aucune colonne trouvée."
        else:
            return f"Erreur lors de l'exécution : {status_response.get('Error', 'Erreur inconnue')}"

    except Exception as e:
        return f"Erreur de connexion ou d'exécution : {str(e)}"


# ---- FONCTION POUR ANALYSER LES TABLES AVEC L'AGENT ----
def agent_analyze_tables():
    """Analyse et décrit chaque table détectée dans Redshift."""
    tables = get_redshift_tables()
    if isinstance(tables, str):
        return tables

    all_tables_info = []
    for table in tables:
        columns = get_table_columns(table)
        all_tables_info.append(f"Table: {table}\nColonnes: {', '.join(columns)}")

    # Construire le prompt pour Mistral AI
    prompt = f"""
    Tu es un expert en bases de données. Analyse et décris chacune des tables trouvées dans Amazon Redshift.
    
    Voici les informations trouvées :
    {chr(10).join(all_tables_info)}

    Pour chaque table :
    1. Donne son rôle dans la base de données.
    2. Explique à quoi sert chaque colonne.
    
    Réponds de manière simple et concise, chaque description de colonne doit être de la même longueur et la plus courte et complète possible.
    """
    print("📢 Prompt envoyé à Mistral :\n", prompt)

    return analyze_with_mistral(prompt)



# ---- FONCTION POUR INTERAGIR AVEC MISTRAL AI ----
def analyze_with_mistral(prompt):
    """Envoie un prompt à Mistral AI via Amazon Bedrock."""
    request_body = {
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0.3,
        "top_p": 0.9
    }

    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(request_body)
    )

    response_body = json.loads(response["body"].read())
    return response_body.get("outputs", [{}])[0].get("text", "")

rep_prompt1 = agent_analyze_tables()

# response = agent_analyze_tables()
# PROMPT 2

def get_table_sample(table_name):
    """Récupère 1000 lignes d'une table Redshift pour analyse."""
    sql_query = f"SELECT * FROM {table_name} LIMIT 100;"
    
    try:
        print(f"🔄 Envoi de la requête à Redshift: {sql_query}")
        response = redshift_client.execute_statement(
            Database=DATABASE,
            WorkgroupName=WORKGROUP_NAME,
            Sql=sql_query
        )

        statement_id = response['Id']
        print(f"✅ Requête envoyée, ID: {statement_id}")

        # Timeout après 60 secondes
        start_time = time.time()
        while True:
            status_response = redshift_client.describe_statement(Id=statement_id)
            status = status_response["Status"]

            if status in ["FINISHED", "FAILED", "ABORTED"]:
                break
            
            # Vérification du timeout (60 secondes max)
            if time.time() - start_time > 60:
                print("⏳ Timeout dépassé (60s). Annulation de la requête.")
                return "Timeout: La requête a pris trop de temps."

            print("⏳ En attente des résultats...")
            time.sleep(3)  # Vérification toutes les 3 secondes

        if status == "FINISHED":
            print("✅ Requête terminée, récupération des résultats...")
            result_response = redshift_client.get_statement_result(Id=statement_id)
            records = [
                ", ".join([col.get('stringValue', 'NULL') for col in row])
                for row in result_response.get("Records", [])
            ]
            return records if records else "Aucune donnée trouvée."
        else:
            print(f"❌ Erreur d'exécution: {status}")
            return f"Erreur lors de l'exécution: {status_response.get('Error', 'Erreur inconnue')}"

    except Exception as e:
        print(f"❌ Erreur de connexion ou d'exécution : {str(e)}")
        return f"Erreur : {str(e)}"


# ---- FONCTION POUR DÉTECTER LES ANOMALIES ----
def agent_detect_anomalies(table_name):
    """Détecte les anomalies d'une table spécifique dans Redshift via Mistral AI."""
    table_sample = get_table_sample(table_name)
    
    if isinstance(table_sample, str):
        return table_sample  # Si erreur, on la renvoie directement

    formatted_sample = "\n".join(table_sample)

    # Construction du prompt
    prompt = f"""
    Tu es un expert en qualité des données.
    {rep_prompt1}
    
    Voici un échantillon de la table "{table_name}":
    {formatted_sample}
    
    Identifie les anomalies (valeurs nulles, doublons, erreurs de format, etc.).
    Génère une requête SQL pour afficher les lignes contenant des données incorrectes.

    Réponds en suivant ce format :
    - *Type d'anomalie* : [Catégorie de l'anomalie]
    - *Description* : [Brève explication]
    - *Requête SQL* : [Requête pour afficher les données erronées]
    """

    return analyze_with_mistral(prompt)


# ---- FONCTION POUR INTERAGIR AVEC MISTRAL AI ----
def analyze_with_mistral(prompt):
    """Envoie un prompt à Mistral AI via Amazon Bedrock."""
    request_body = {
        "prompt": prompt,
        "max_tokens": 3000,
        "temperature": 0.3,
        "top_p": 0.9
    }

    try:
        print("🔄 Envoi du prompt à Mistral AI...")
        response = bedrock_client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body)
        )
        print("✅ Réponse reçue de Mistral.")

        response_body = json.loads(response["body"].read())
        return response_body.get("outputs", [{}])[0].get("text", "")

    except Exception as e:
        print(f"❌ Erreur d'interaction avec Mistral AI : {str(e)}")
        return f"Erreur : {str(e)}"

def execute_sql_query(query):
    """Exécute une requête SQL sur Redshift et retourne les résultats."""
    try:
        response = redshift_client.execute_statement(
            Database=DATABASE,
            WorkgroupName=WORKGROUP_NAME,
            Sql=query
        )

        statement_id = response['Id']
        while True:
            status_response = redshift_client.describe_statement(Id=statement_id)
            status = status_response["Status"]
            if status in ["FINISHED", "FAILED", "ABORTED"]:
                break
            time.sleep(2)

        if status == "FINISHED":
            result_response = redshift_client.get_statement_result(Id=statement_id)
            rows = [
                {col['name']: row[i].get('stringValue', 'NULL') for i, col in enumerate(result_response['ColumnMetadata'])}
                for row in result_response.get("Records", [])
            ]
            return pd.DataFrame(rows) if rows else "Aucun résultat trouvé."
        else:
            return f"Erreur lors de l'exécution : {status_response.get('Error', 'Erreur inconnue')}"

    except Exception as e:
        return f"Erreur de connexion ou d'exécution : {str(e)}"
