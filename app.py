import streamlit as st
import backend  # Ensure backend.py is in the same directory
import json

# Configuration de la page
st.set_page_config(
    page_title="Veolia Data Quality AI",
    page_icon="🔍",
    layout="wide"
)

# Stocker la description des tables en mémoire (une seule fois)
if 'rep_prompt1' not in st.session_state:
    st.session_state.rep_prompt1 = backend.agent_analyze_tables()

# Titre principal
st.markdown("<h1 class='header'>🔍 Veolia - Analyse et Qualité des Données</h1>", unsafe_allow_html=True)

# Onglets
tab1, tab2, tab3, tab4 = st.tabs([
    "🏷️ Description des Tables",
    "🚨 Détection d'Anomalies",
    "🤖 Analyse IA avec Mistral",
    "📊 Exécution des Requêtes SQL"
])

# --- Onglet 1 : Description des Tables ---
with tab1:
    st.subheader("📊 Structure des Tables Redshift")
    tables = backend.get_redshift_tables()

    for table in tables:
        with st.expander(f"📌 Table **{table}**", expanded=False):
            columns = backend.get_table_columns(table)
            for col in columns:
                st.markdown(f"- **{col}**")

            if st.button(f"🔎 Voir un extrait ({table})", key=f"sample_{table}"):
                sample_data = backend.get_table_sample(table)
                st.dataframe(sample_data, height=250, use_container_width=True)

    # Afficher la description des tables provenant de Mistral
    st.subheader("📑 Description des tables et colonnes")
    st.markdown(st.session_state.rep_prompt1)

# --- Onglet 2 : Détection d'Anomalies ---
with tab2:
    st.subheader("🚨 Analyse et Détection d'Anomalies")
    
    table_name = st.selectbox("Sélectionnez une table", backend.get_redshift_tables())
    
    if st.button("📊 Analyser les anomalies", key="detect_anomalies"):
        anomalies = backend.agent_detect_anomalies(table_name)
        
        # 💡 Correction pour bien formater la sortie JSON
        if isinstance(anomalies, dict):
            st.json(anomalies)
        else:
            st.write(anomalies)  # Affichage brut de l'IA pour validation


# --- Onglet 3 : Analyse avec Mistral AI ---
with tab3:
    st.subheader("🤖 Analyse IA avec Mistral")
    user_query = st.text_area("Décrivez votre requête AI :", "Détecte les incohérences entre consommation et facturation.")

    if st.button("🚀 Envoyer à Mistral AI", key="mistral_prompt"):
        final_prompt = f"""
        Voici les informations de la base de données :

        {st.session_state.rep_prompt1}

        Maintenant, réponds uniquement à cette question : {user_query}
        """

        ai_response = backend.analyze_with_mistral(final_prompt)
        st.text_area("💡 Réponse de l'IA :", ai_response, height=200)

# --- Onglet 4 : Exécution des Requêtes SQL ---
with tab4:
    st.subheader("📊 Exécution des Requêtes SQL")

    sql_query = st.text_area("Entrez une requête SQL à exécuter :", "")

    if st.button("🚀 Exécuter la requête", key="execute_sql") and sql_query.strip():
        query_result = backend.execute_sql_query(sql_query)
        if isinstance(query_result, str):
            st.error(f"Erreur lors de l'exécution : {query_result}")
        else:
            st.dataframe(query_result.head(5), height=250, use_container_width=True)

# --- Sidebar Chatbot IA ---
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Assistant IA de Vérification des Données")
user_input = st.sidebar.text_input("Posez votre question...")
if user_input:
    with st.sidebar:
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            final_prompt = f"""
            Voici les informations de la base de données :

            {st.session_state.rep_prompt1}

            Maintenant, réponds uniquement à cette question : {user_input}
            """
            ai_answer = backend.analyze_with_mistral(final_prompt)
            st.markdown(ai_answer)
