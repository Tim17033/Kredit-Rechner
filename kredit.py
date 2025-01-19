import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import math

# Zinssatz basierend auf dem Kreditbetrag
def get_interest_rate(kreditbetrag):
    if 2500 <= kreditbetrag < 5000:
        return 0.095
    elif 5000 <= kreditbetrag < 10000:
        return 0.079
    elif 10000 <= kreditbetrag <= 50000:
        return 0.068
    else:
        return None

# Berechnung der monatlichen Rate (Annuität)
def calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit):
    r = zinssatz / 12
    n = laufzeit * 12
    annuitaet = kreditbetrag * (r * (1 + r)**n) / ((1 + r)**n - 1)
    return annuitaet

# Berechnung der Restschuld nach Zinsbindungsfrist
def calculate_restschuld(kreditbetrag, zinssatz, laufzeit, zinsbindung):
    r = zinssatz / 12
    n = laufzeit * 12
    zinsbindung_monate = zinsbindung * 12
    restschuld = kreditbetrag * ((1 + r)**n - (1 + r)**zinsbindung_monate) / ((1 + r)**n - 1)
    return restschuld

# UI-Design
st.title("📊 Kreditverkaufsrechner")
st.markdown(
    """
    Willkommen beim Kreditverkaufsrechner! Berechnen Sie schnell und einfach die monatliche Rate für Ihren Kunden, 
    inklusive der Aufschlüsselung in Zins und Tilgung. 🚀✨
    """
)

# Eingabefelder
kreditbetrag = st.number_input("Finanzierungsbedarf (€):", min_value=2500, max_value=50000, step=100)
laufzeit = st.number_input("Gewünschte Laufzeit (in Jahren):", min_value=1, max_value=20, step=1)
zinsbindung = st.selectbox("Zinsbindungsfrist:", options=[5, 10])
kapitaldienst = st.number_input("Aktueller Kapitaldienst (€):", min_value=0.0, step=50.0)
rkv_option = st.radio("Möchten Sie eine Ratenkreditversicherung (RKV) hinzufügen?", options=["Ja", "Nein"])

if st.button("Berechnung starten"):
    with st.spinner("Berechnung wird durchgeführt..."):
        time.sleep(2)  # Simulierte Ladezeit

    zinssatz = get_interest_rate(kreditbetrag)
    if zinssatz is None:
        st.error("Bitte geben Sie einen Kreditbetrag zwischen 2.500 € und 50.000 € ein.")
    else:
        monatliche_rate = calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit)
        restschuld = calculate_restschuld(kreditbetrag, zinssatz, laufzeit, zinsbindung)

        # RKV-Berechnung
        rkv_aufschlag = kreditbetrag * 0.00273
        monatliche_rate_mit_rkv = monatliche_rate + rkv_aufschlag

        # Überprüfung des Kapitaldienstes
        if monatliche_rate > kapitaldienst:
            laufzeit += 1  # Laufzeit anpassen
            st.warning("Hey, mit ein wenig mehr Laufzeit passt es! Die Laufzeit wurde automatisch angepasst.")

        # Zins- und Tilgungsanteile auflisten
        zins_anteil = kreditbetrag * (zinssatz / 12)
        tilgung_anteil = monatliche_rate - zins_anteil

        st.success(f"🎉 Monatliche Rate: {monatliche_rate:.2f} €")
        st.markdown(f"💼 **Monatliche Rate (mit RKV): {monatliche_rate_mit_rkv:.2f} €**")
        st.markdown(f"📉 **Restschuld nach {zinsbindung} Jahren: {restschuld:,.2f} €**")

        # Zins- und Tilgungstabelle
        data = {
            "Monat": list(range(1, laufzeit * 12 + 1)),
            "Zinsanteil (€)": [zins_anteil] * (laufzeit * 12),
            "Tilgungsanteil (€)": [tilgung_anteil] * (laufzeit * 12),
        }
        df = pd.DataFrame(data)
        st.dataframe(df.head(12))

        # Grafische Darstellung
        fig, ax = plt.subplots()
        ax.bar(df["Monat"][:12], df["Zinsanteil (€)"][:12], label="Zinsanteil")
        ax.bar(df["Monat"][:12], df["Tilgungsanteil (€)"][:12], bottom=df["Zinsanteil (€)"][:12], label="Tilgungsanteil")
        ax.set_title("Zins- und Tilgungsverlauf (1. Jahr)")
        ax.set_xlabel("Monat")
        ax.set_ylabel("Betrag (€)")
        ax.legend()
        st.pyplot(fig)
