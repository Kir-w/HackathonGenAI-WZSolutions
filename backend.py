import boto3
import json
import time
import pandas as pd
from typing import List, Dict, Union

# Configuration AWS
AWS_REGION = "us-west-2"
REDSHIFT_WORKGROUP = "wz-solutions-redshift-workgroup"
REDSHIFT_DATABASE = "dev"
BEDROCK_MODEL_ID = "amazon.titan-text-express-v1"

# Initialisation des clients AWS
redshift_client = boto3.client('redshift-data', region_name=AWS_REGION)
bedrock_client = boto3.client('bedrock-runtime', region_name=AWS_REGION)

def execute_redshift_query(sql_query: str) -> pd.DataFrame:
    """Exécute une requête SQL sur Redshift et retourne les résultats"""
    try:
        response = redshift_client.execute_statement(
            Database=REDSHIFT_DATABASE,
            WorkgroupName=REDSHIFT_WORKGROUP,
            Sql=sql_query
        )
        
        statement_id = response['Id']
        
        while True:
            status = redshift_client.describe_statement(Id=statement_id)['Status']
            if status in ['FINISHED', 'FAILED', 'ABORTED']:
                break
            time.sleep(2)
            
        if status == 'FINISHED':
            result = redshift_client.get_statement_result(Id=statement_id)
            columns = [col['name'] for col in result['ColumnMetadata']]
            rows = [[list(field.values())[0] for field in record] for record in result['Records']]
            return pd.DataFrame(rows, columns=columns)
            
        raise Exception(f"Query failed: {status}")
        
    except Exception as e:
        raise RuntimeError(f"Redshift error: {str(e)}")

def analyze_with_bedrock(prompt: str, max_tokens: int = 300) -> str:
    """Utilise Amazon Bedrock pour analyser les données"""
    try:
        request_body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": 0,
                "topP": 1,
                "stopSequences": []
            }
        }
        
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body.get('results', [{}])[0].get('outputText', '')
        
    except Exception as e:
        raise RuntimeError(f"Bedrock error: {str(e)}")

def get_table_schema(table_name: str) -> Dict:
    """Récupère le schéma d'une table"""
    query = f"""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = '{table_name}';
    """
    result = execute_redshift_query(query)
    return {
        "table_name": table_name,
        "columns": result.set_index('column_name')['data_type'].to_dict()
    }

def detect_data_anomalies(table_name: str) -> List[Dict]:
    """Détecte les anomalies dans une table"""
    # Analyse avec Bedrock
    schema = get_table_schema(table_name)
    sample_data = execute_redshift_query(f"SELECT * FROM {table_name} LIMIT 10;")
    
    prompt = f"""
    Analyse cette structure de table et ces données pour détecter des anomalies:
    
    Table: {schema['table_name']}
    Colonnes: {schema['columns']}
    
    Données échantillon:
    {sample_data.to_markdown()}
    
    Génère:
    1. Une liste d'anomalies potentielles
    2. Les requêtes SQL pour les identifier
    3. Des recommandations de correction
    """
    
    analysis = analyze_with_bedrock(prompt)
    
    # Formatage des résultats
    return parse_analysis_results(analysis)

def parse_analysis_results(raw_analysis: str) -> List[Dict]:
    """Transforme la sortie texte de Bedrock en structure de données"""
    # Cette fonction dépend du format de sortie de votre modèle
    # Exemple d'implémentation basique :
    anomalies = []
    current_anomaly = {}
    
    for line in raw_analysis.split('\n'):
        if line.startswith("- Anomalie"):
            if current_anomaly:
                anomalies.append(current_anomaly)
            current_anomaly = {"description": line[2:]}
        elif line.startswith("  Requête SQL:"):
            current_anomaly["query"] = line.split(":")[1].strip()
        elif line.startswith("  Recommandation:"):
            current_anomaly["recommendation"] = line.split(":")[1].strip()
    
    if current_anomaly:
        anomalies.append(current_anomaly)
        
    return anomalies

def generate_data_quality_report(table_name: str) -> Dict:
    """Génère un rapport complet de qualité des données"""
    schema = get_table_schema(table_name)
    anomalies = detect_data_anomalies(table_name)
    
    return {
        "table_name": table_name,
        "schema": schema,
        "anomalies": anomalies,
        "summary": {
            "total_anomalies": len(anomalies),
            "critical_issues": sum(1 for a in anomalies if "critique" in a.get("description", "").lower())
        }
    }

# Fonctions supplémentaires de l'agent
def list_redshift_tables() -> List[str]:
    """Liste toutes les tables disponibles"""
    query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
    result = execute_redshift_query(query)
    return result['tablename'].tolist()

def get_table_sample(table_name: str, limit: int = 10) -> pd.DataFrame:
    """Récupère un échantillon de données d'une table"""
    return execute_redshift_query(f"SELECT * FROM {table_name} LIMIT {limit};")

def explain_sql_query(query: str) -> str:
    """Explique une requête SQL avec Bedrock"""
    prompt = f"""
    Explique cette requête SQL en français simple :
    
    {query}
    
    Inclus :
    - Le but de la requête
    - Les tables impliquées
    - Les conditions importantes
    - Les colonnes retournées
    """
    return analyze_with_bedrock(prompt)