import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
        # Berechnungen
        monatliche_rate = calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit)
        restschuld = calculate_restschuld(kreditbetrag, zinssatz, laufzeit, zinsbindung)
        zins_anteil = kreditbetrag * (zinssatz / 12)
        tilgung_anteil = monatliche_rate - zins_anteil
        anfaenglicher_tilgungsprozentsatz = (tilgung_anteil / kreditbetrag) * 100
        zinsprozentsatz = zinssatz * 100

        # RKV-Berechnung
        rkv_aufschlag = kreditbetrag * 0.00273
        monatliche_rate_mit_rkv = monatliche_rate + rkv_aufschlag

        # Ausgabe der Ergebnisse
        st.success(f"🎉 Monatliche Rate: {monatliche_rate:.2f} €")
        st.markdown(f"💼 **Monatliche Rate (mit RKV): {monatliche_rate_mit_rkv:.2f} €**")
        st.markdown(f"📉 **Restschuld nach {zinsbindung} Jahren: {restschuld:,.2f} €**")
        st.markdown(f"💰 **Zinsanteil der monatlichen Rate: {zins_anteil:.2f} €**")
        st.markdown(f"💸 **Tilgungsanteil der monatlichen Rate: {tilgung_anteil:.2f} €**")
        st.markdown(f"🔍 **Anfänglicher Zinssatz: {zinsprozentsatz:.2f}%**")
        st.markdown(f"📊 **Anfänglicher Tilgungssatz: {anfaenglicher_tilgungsprozentsatz:.2f}%**")

        # Visualisierung 1: Zins- und Tilgungsentwicklung
        monate = list(range(1, laufzeit * 12 + 1))
        zins_anteile = []
        tilgungs_anteile = []
        restschuld = kreditbetrag

        for monat in monate:
            zins = restschuld * (zinssatz / 12)
            tilgung = monatliche_rate - zins
            restschuld -= tilgung
            zins_anteile.append(zins)
            tilgungs_anteile.append(tilgung)

        fig1, ax1 = plt.subplots()
        ax1.plot(monate, zins_anteile, label="Zinsanteil", color="red")
        ax1.plot(monate, tilgungs_anteile, label="Tilgungsanteil", color="blue")
        ax1.set_title("Entwicklung von Zins- und Tilgungsanteilen")
        ax1.set_xlabel("Monate")
        ax1.set_ylabel("Betrag (€)")
        ax1.legend()
        ax1.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(fig1)

        # Visualisierung 2: Kreisdiagramm (Zins vs Tilgung)
        fig2, ax2 = plt.subplots()
        ax2.pie(
            [zins_anteil, tilgung_anteil],
            labels=["Zinsanteil", "Tilgungsanteil"],
            autopct="%1.1f%%",
            startangle=90,
            colors=["#ff9999", "#66b3ff"],
        )
        ax2.axis("equal")  # Kreisdiagramm rund darstellen
        st.pyplot(fig2)


