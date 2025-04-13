
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ankaufsprozess Template App", layout="wide")
st.title("Ankaufsprozess: Upload & Monatsübersicht")

DATA_FILE = "vorgaenge.csv"

# --- Formular zur Eingabe eines neuen Vorgangs ---
st.header("Neuen Vorgang erfassen")

with st.form("vorgang_form"):
    fondsname = st.text_input("Fondsname")
    transaktionsart = st.selectbox("Transaktionsart", ["Ankauf", "Verkauf", "Sonstiges"])
    betrag = st.number_input("Betrag in EUR", min_value=0.0, format="%.2f")
    gebuehrenrelevant = st.selectbox("Gebührenrelevant?", ["Ja", "Nein"])
    dateiupload = st.file_uploader("Datei hochladen (optional)", type=["pdf", "zip", "docx", "xlsx"])
    submitted = st.form_submit_button("Vorgang speichern")

# --- Vorgang speichern ---
if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([{
        "Zeitpunkt": timestamp,
        "Fondsname": fondsname,
        "Transaktionsart": transaktionsart,
        "Betrag": betrag,
        "Gebührenrelevant": gebuehrenrelevant,
        "Dateiname": dateiupload.name if dateiupload else ""
    }])

    if os.path.exists(DATA_FILE):
        existing = pd.read_csv(DATA_FILE)
        combined = pd.concat([existing, new_data], ignore_index=True)
    else:
        combined = new_data

    combined.to_csv(DATA_FILE, index=False)
    st.success("Vorgang erfolgreich gespeichert!")

# --- Bestehende Vorgänge anzeigen ---
st.header("Erfasste Vorgänge")
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
    st.dataframe(data)

    # Download-Button
    csv = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Monatsliste herunterladen (CSV)",
        data=csv,
        file_name="monatsliste.csv",
        mime="text/csv"
    )
else:
    st.info("Noch keine Vorgänge erfasst.")
