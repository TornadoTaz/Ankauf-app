
import streamlit as st

st.set_page_config(page_title="Ankaufsprozess Visualisierung", layout="wide")

st.title("Ablauf: Ankaufsvorschlag bis Monatsreport")

st.markdown("## 1. Ankaufsvorschlag")
st.write("- Anlageberater erstellt Ankaufsvorschlag")
st.write("- Optional: Template herunterladen und wieder hochladen")

st.markdown("## 2. Eingang bei AIFM")
st.write("- Anlagevorschlag geht an AIFM")
st.write("- Portfoliomanagement erstellt Decision Sheet mit allen relevanten Informationen")

st.markdown("## 3. Prüfung durch Fachabteilungen")
st.write("- Decision Sheet geht an Fachabteilungen")
st.write("- Fachabteilungen führen Prüfungen durch und laden ihre Ergebnisse hoch")

st.markdown("## 4. Freigabephase")
st.write("- Geschäftsführung erhält das Prüfsheet")
st.write("- Freigabeprozess wird durchgeführt")

st.markdown("## 5. Transaktion")
st.write("- Transaktion wird angestoßen")
st.write("- Verträge werden hochgeladen und an Zeichnungsberechtigte gesendet")

st.markdown("## 6. Nach der Zeichnung")
st.write("- Zeichnung wird bestätigt, Daten gehen zurück an Portfoliomanagement")
st.write("- Portfoliomanagement informiert Investment Operations")

st.markdown("## 7. Zahlung & Abschluss")
st.write("- Investment Operations führt die Zahlung aus")
st.write("- Kompletter Vorgang geht an Depotbank und Zentralverwaltung")
st.write("- Eine ZIP-Datei des Vorgangs wird erstellt")

st.markdown("## 8. Monatliche Zusammenfassung")
st.write("- Alle Vorgänge werden monatlich zusammengefasst")
st.write("- Enthalten: Fondsname, Transaktionsart, Betrag, Gebührenrelevanz")

st.markdown("---")
st.markdown("## Dokumente hochladen")

uploaded_file = st.file_uploader("Bitte lade eine Datei hoch", type=["pdf", "docx", "xlsx", "zip"])
if uploaded_file is not None:
    st.success(f"Datei '{uploaded_file.name}' wurde erfolgreich hochgeladen!")

st.markdown("## Vorlage oder ZIP-Datei herunterladen")

with open("vorlage.zip", "rb") as file:
    st.download_button(
        label="Vorlage herunterladen",
        data=file,
        file_name="vorlage.zip",
        mime="application/zip"
    )

st.success("Upload- & Download-Funktionen sind aktiv!")
