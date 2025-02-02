import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Veolia Data Analyst",
    page_icon="🔍",
    layout="wide"
)

# Style personnalisé
st.markdown("""
<style>
    .header { color: #1f5673; font-weight: 700; }
    .stExpander { border: 1px solid #e1e4e8 !important; border-radius: 10px !important; }
    .stButton>button { background-color: #1f5673 !important; color: white !important; }
    .sql-box { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("<h1 class='header'>🔍 Veolia - Analyse des Données Redshift</h1>", unsafe_allow_html=True)

# Onglets pour les différentes étapes
tab1, tab2, tab3 = st.tabs([
    "🏷️ Description des Tables", 
    "🚨 Détection d'Anomalies", 
    "🔎 Résultats des Requêtes"
])

# Données simulées (à remplacer par les appels à votre backend)
SAMPLE_TABLES = {
    "abonnements": {
        "description": "Table contenant les informations sur les abonnements des clients",
        "columns": {
            "cle_abonnement": "Identifiant unique de l'abonnement",
            "date_entree_local_abonnement": "Date de début de l'abonnement",
            "date_resiliation_abo": "Date de résiliation de l'abonnement"
        }
    },
    "consommations": {
        "description": "Table des données de consommation mensuelle des clients",
        "columns": {
            "volume_mois": "Volume consommé durant le mois",
            "diametre_nominal": "Diamètre du compteur d'eau"
        }
    }
}

SAMPLE_ANOMALIES = [
    {
        "query": "SELECT * FROM abonnements WHERE date_resiliation_abo < date_entree_local_abonnement;",
        "description": "Dates de résiliation antérieures aux dates de début de contrat",
        "sample_data": [
            ["ABN_001", "2023-01-01", "2022-12-31"],
            ["ABN_002", "2023-02-15", "2023-01-30"]
        ]
    },
    {
        "query": "SELECT * FROM consommations WHERE volume_mois < 0;",
        "description": "Volumes de consommation négatifs détectés",
        "sample_data": [
            ["CONS_001", -5.2, 15.0],
            ["CONS_002", -1.8, 20.0]
        ]
    }
]

# Onglet 1 - Description des tables
with tab1:
    st.subheader("Analyse Structurelle des Tables")
    
    for table_name, table_info in SAMPLE_TABLES.items():
        with st.expander(f"📊 Table **{table_name}**", expanded=True):
            st.markdown(f"**Description :** {table_info['description']}")
            st.markdown("**Structure des colonnes :**")
            for col_name, col_desc in table_info["columns"].items():
                st.markdown(f"- `{col_name}` : {col_desc}")

# Onglet 2 - Détection d'anomalies
with tab2:
    st.subheader("Requêtes de Détection d'Anomalies")
    
    for idx, anomaly in enumerate(SAMPLE_ANOMALIES, 1):
        with st.expander(f"Anomalie #{idx} - {anomaly['description']}", expanded=True):
            st.markdown("```sql\n" + anomaly["query"] + "\n```")
            st.markdown(f"**Raison :** {anomaly['description']}")
            if st.button(f"Voir les résultats ▶️", key=f"btn_{idx}"):
                st.session_state.selected_anomaly = anomaly

# Onglet 3 - Résultats des requêtes
with tab3:
    if 'selected_anomaly' in st.session_state:
        anomaly = st.session_state.selected_anomaly
        st.subheader("Résultats de l'Analyse")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("**Requête exécutée :**")
            st.code(anomaly["query"], language='sql')
            
        with col2:
            st.markdown("**Exemple de données problématiques :**")
            st.dataframe(
                pd.DataFrame(
                    anomaly["sample_data"],
                    columns=["ID", "Date Début", "Date Fin"] if "abonnements" in anomaly["query"] 
                    else ["ID", "Volume", "Diamètre"]
                ),
                height=200,
                use_container_width=True
            )
    else:
        st.info("ℹ️ Sélectionnez une anomalie dans l'onglet précédent pour afficher les résultats")

# Section chatbot
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Assistant Data Analyst")

# Simulation de l'agent conversationnel
user_input = st.sidebar.text_input("Posez votre question ici...")

if user_input:
    with st.sidebar:
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            st.markdown("""
            Voici un exemple de réponse de l'agent :
            
            ```sql
            SELECT * 
            FROM consommations 
            WHERE volume_mois > 1000 
            AND diametre_nominal < 15;
            ```
            
            **Explication** : Détection des consommations anormalement élevées pour des petits diamètres
            """)