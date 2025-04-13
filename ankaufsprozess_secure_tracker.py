
# © 2025 Max Mustermann – Alle Rechte vorbehalten
# Dieses Script ist urheberrechtlich geschützt. Eine Veränderung des Kopfbereichs ohne Zustimmung des Autors ist untersagt.

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Ankaufsprozess Tracker", layout="wide")
st.title("Ankaufsprozess: Vorgänge & Fortschritt")

DATA_FILE = "vorgaenge_status.csv"
UPLOAD_FOLDER = "uploads"
TEMPLATE_FOLDER = "templates"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)

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

schritte_mit_upload = [0, 1, 2, 6, 7]  # Schritte mit Datei-Upload + Template

# Dummy-Templates bereitstellen (einmalig)
for i in schritte_mit_upload:
    pfad = os.path.join(TEMPLATE_FOLDER, f"template_schritt_{i+1}.txt")
    if not os.path.exists(pfad):
        with open(pfad, "w") as f:
            f.write(f"Dies ist das Template für Schritt {i+1}: {prozess_schritte[i]}")

# Formular zur Erfassung eines neuen Vorgangs
st.header("Neuen Vorgang erfassen")
with st.form("neuer_vorgang"):
    fondsname = st.text_input("Fondsname")
    transaktionsart = st.selectbox("Transaktionsart", ["Ankauf", "Verkauf", "Sonstiges"])
    betrag = st.number_input("Betrag in EUR", min_value=0.0, format="%.2f")
    gebuehrenrelevant = st.selectbox("Gebührenrelevant?", ["Ja", "Nein"])
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
    }
    for schritt in prozess_schritte:
        vorgang[schritt] = False
    for i in schritte_mit_upload:
        vorgang[f"Upload_{i}"] = ""

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

    for i, schritt in enumerate(prozess_schritte):
        col1, col2 = st.columns([3, 2])
        with col1:
            # Zeige Checkbox (aber deaktiviert, wenn automatisch)
            manuell_setzbar = i not in schritte_mit_upload
            checked = bool(vorgang[schritt])
            if manuell_setzbar:
                neu = st.checkbox(schritt, value=checked, key=schritt)
                df.at[idx, schritt] = neu
            else:
                st.checkbox(schritt, value=checked, key=schritt, disabled=True)

        if i in schritte_mit_upload:
            with col2:
                template_path = os.path.join(TEMPLATE_FOLDER, f"template_schritt_{i+1}.txt")
                with open(template_path, "rb") as tfile:
                    st.download_button(f"Template Schritt {i+1}", tfile.read(), file_name=os.path.basename(template_path))

                upload_key = f"Upload_{i}"
                file = st.file_uploader(f"Datei für Schritt {i+1} hochladen", key=f"upload_{i}")
                if file:
                    save_path = os.path.join(UPLOAD_FOLDER, f"{vorgang['Fondsname']}_S{i+1}_{file.name}")
                    with open(save_path, "wb") as f:
                        f.write(file.read())
                    df.at[idx, schritt] = True
                    df.at[idx, upload_key] = file.name
                    st.success("Datei gespeichert & Schritt abgeschlossen")

        if df.at[idx, schritt]:
            abgeschlossen += 1
        else:
            offene.append(schritt)

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
