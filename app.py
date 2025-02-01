import streamlit as st
import pandas as pd

# 🎨 UI Setup
st.set_page_config(page_title="Anomaly Detector - Veolia", layout="wide")

st.title("🔍 Anomaly Detector - Veolia")
st.markdown("### Analyse des données et génération de requêtes SQL")

# Sidebar pour les options
st.sidebar.header("Options")
uploaded_file = st.sidebar.file_uploader("📂 Importer un dataset", type=["csv", "xlsx"])

# Affichage des anomalies détectées
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Aperçu des données")
    st.dataframe(df.head(10), use_container_width=True)

    # Simuler des anomalies (remplacer par votre backend)
    anomalies = df.sample(3)  # Simule 3 anomalies
    st.subheader("⚠️ Anomalies détectées")
    st.dataframe(anomalies.style.set_properties(**{'background-color': 'rgba(255,0,0,0.2)'}))

    # Simuler une requête SQL en sortie
    sql_query = f"SELECT * FROM dataset WHERE id IN {tuple(anomalies.index)};"
    st.subheader("📝 Requête SQL générée")
    st.code(sql_query, language="sql")