import pandas as pd
from transformers import pipeline
from config import execute_query, invoke_agent

# Fonction pour vérifier la continuité des consommations
def check_continuity(client_id, start_year):
    query = f"""
    SELECT *
    FROM consommation
    WHERE client_id = '{client_id}' AND EXTRACT(YEAR FROM date) >= {start_year}
    ORDER BY date;
    """
    return query

# Fonction pour deviner le type de données
def guess_data_type(column_name, sample_data):
    # Utiliser un modèle de langage pour deviner le type de données
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    candidate_labels = ["date", "numeric", "text", "boolean"]
    result = classifier(f"{column_name}: {sample_data}", candidate_labels)
    return result['labels'][0]

# Fonction pour invoquer l'agent AI et obtenir une réponse
def get_agent_response(prompt):
    response = invoke_agent(prompt)
    if response:
        return response['response']
    else:
        return "Erreur lors de l'invocation de l'agent."
