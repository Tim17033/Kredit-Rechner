import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

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

# Berechnung der Zins- und Tilgungsanteile über die Laufzeit
def calculate_zins_tilgung(kreditbetrag, zinssatz, laufzeit, monatliche_rate):
    zins_anteile = []
    tilgungs_anteile = []
    restschuld = kreditbetrag

    for _ in range(laufzeit * 12):
        zins = restschuld * (zinssatz / 12)
        tilgung = monatliche_rate - zins
        restschuld -= tilgung
        zins_anteile.append(zins)
        tilgungs_anteile.append(tilgung)

    return zins_anteile, tilgungs_anteile

# UI-Design
st.title("📊 Kreditverkaufsrechner")
st.markdown(
    """
    Willkommen beim Kreditverkaufsrechner! Berechnen Sie schnell und einfach die monatliche Rate für Ihren Kunden, 
    inklusive der Zins- und Tilgungsanteile. 🚀✨
    """
)

# Eingabefelder
kreditbetrag = st.number_input("Finanzierungsbedarf (€):", min_value=2500, max_value=50000, step=100)
laufzeit = st.number_input("Gewünschte Laufzeit (in Jahren):", min_value=1, max_value=20, step=1)
rkv_option = st.radio("Möchten Sie eine Ratenkreditversicherung (RKV) hinzufügen?", options=["Ja", "Nein"])

if st.button("Berechnung starten"):
    with st.spinner("Berechnung wird durchgeführt..."):
        time.sleep(2)  # Simulierte Ladezeit

    zinssatz = get_interest_rate(kreditbetrag)
    if zinssatz is None:
        st.error("Bitte geben Sie einen Kreditbetrag zwischen 2.500 € und 50.000 € ein.")
    else:
        # Berechnungen
        monatliche_rate = calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit)
        zins_anteil = kreditbetrag * (zinssatz / 12)
        tilgung_anteil = monatliche_rate - zins_anteil
        anfaenglicher_tilgungsprozentsatz = (tilgung_anteil / kreditbetrag) * 100
        zinsprozentsatz = zinssatz * 100

        # RKV-Berechnung
        rkv_aufschlag = kreditbetrag * 0.00273
        monatliche_rate_mit_rkv = monatliche_rate + rkv_aufschlag

        # Berechnung der Zins- und Tilgungsanteile
        zins_anteile, tilgungs_anteile = calculate_zins_tilgung(kreditbetrag, zinssatz, laufzeit, monatliche_rate)

        # Besondere Hervorhebung der Ergebnisse
        st.markdown(
            f"""
            ## 🏦 Ergebnisse
            - 💰 **Monatliche Rate (ohne RKV): {monatliche_rate:.2f} €**
            - 📉 **Monatliche Rate (mit RKV): {monatliche_rate_mit_rkv:.2f} €**
            - 🔍 **Anfänglicher Zinssatz: {zinsprozentsatz:.2f}%**
            - 📊 **Anfänglicher Tilgungssatz: {anfaenglicher_tilgungsprozentsatz:.2f}%**
            """
        )

        # Visualisierung: Zins- und Tilgungsanteile als Balkendiagramm
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(1, 13)  # Ersten 12 Monate
        ax.bar(x, zins_anteile[:12], label="Zinsen", color="gray", alpha=0.7)
        ax.bar(x, tilgungs_anteile[:12], bottom=zins_anteile[:12], label="Tilgung", color="orange", alpha=0.9)
        ax.set_title("Zins- und Tilgungsanteile im ersten Jahr", fontsize=16)
        ax.set_xlabel("Monat", fontsize=12)
        ax.set_ylabel("Betrag (€)", fontsize=12)
        ax.legend()
        st.pyplot(fig)




