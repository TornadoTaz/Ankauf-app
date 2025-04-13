
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ankaufsprozess Tracker", layout="wide")
st.title("Ankaufsprozess: Vorgänge & Fortschritt")

DATA_FILE = "vorgaenge_status.csv"

prozess_schritte = [
    "Anlagevorschlag eingereicht",
    "Decision Sheet erstellt",
    "Prüfung durch Fachabteilungen",
    "Freigabe durch Geschäftsführung",
    "Transaktion angestoßen",
    "Verträge versendet",
    "Zeichnung erhalten",
    "Zahlung durchgeführt",
    "Paket an Depotbank",
    "ZIP-Datei erstellt"
]

# Formular zur Erfassung eines neuen Vorgangs
st.header("Neuen Vorgang erfassen")
with st.form("neuer_vorgang"):
    fondsname = st.text_input("Fondsname")
    transaktionsart = st.selectbox("Transaktionsart", ["Ankauf", "Verkauf", "Sonstiges"])
    betrag = st.number_input("Betrag in EUR", min_value=0.0, format="%.2f")
    gebuehrenrelevant = st.selectbox("Gebührenrelevant?", ["Ja", "Nein"])
    dateiupload = st.file_uploader("Datei hochladen", type=["pdf", "docx", "xlsx", "zip"])
    speichern = st.form_submit_button("Vorgang anlegen")

# Vorgang speichern
if speichern:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vorgang = {
        "Zeitpunkt": timestamp,
        "Fondsname": fondsname,
        "Transaktionsart": transaktionsart,
        "Betrag": betrag,
        "Gebührenrelevant": gebuehrenrelevant,
        "Dateiname": dateiupload.name if dateiupload else "",
    }
    for schritt in prozess_schritte:
        vorgang[schritt] = False

    df_neu = pd.DataFrame([vorgang])

    if os.path.exists(DATA_FILE):
        df_alt = pd.read_csv(DATA_FILE)
        df = pd.concat([df_alt, df_neu], ignore_index=True)
    else:
        df = df_neu

    df.to_csv(DATA_FILE, index=False)
    st.success(f"Vorgang für '{fondsname}' wurde angelegt.")

# Bestehende Vorgänge verwalten
if os.path.exists(DATA_FILE):
    st.header("Vorgänge & Fortschritt")

    df = pd.read_csv(DATA_FILE)
    vorgang_liste = df["Fondsname"] + " (" + df["Zeitpunkt"] + ")"
    auswahl = st.selectbox("Vorgang auswählen:", vorgang_liste)

    idx = vorgang_liste[vorgang_liste == auswahl].index[0]
    vorgang = df.loc[idx]

    st.subheader(f"Fortschritt für: {vorgang['Fondsname']}")
    offene = []
    abgeschlossen = 0

    for schritt in prozess_schritte:
        status = bool(vorgang[schritt])
        neu = st.checkbox(schritt, value=status, key=schritt)
        df.at[idx, schritt] = neu
        if not neu:
            offene.append(schritt)
        else:
            abgeschlossen += 1

    fortschritt = int((abgeschlossen / len(prozess_schritte)) * 100)
    st.progress(fortschritt)

    if offene:
        st.warning("Nicht abgeschlossene Schritte:")
        for s in offene:
            st.write(f"- {s}")
    else:
        st.success("Alle Prozessschritte abgeschlossen!")

    df.to_csv(DATA_FILE, index=False)

    # Monatsreport Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Monatsreport herunterladen (CSV)",
        data=csv,
        file_name="monatsreport.csv",
        mime="text/csv"
    )
else:
    st.info("Noch keine Vorgänge vorhanden.")
