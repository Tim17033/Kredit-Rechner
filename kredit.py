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
        zins = restschuld * (zins_pro_jahr / 12)
        tilgung = monatliche_rate - zins
        restschuld -= tilgung
        zins_anteile.append(zins)
        tilgungs_anteile.append(tilgung)

    return zins_anteile, tilgungs_anteile

# Berechnung der Tilgungssätze (monatlich und jährlich)
def calculate_tilgungssaetze(kreditbetrag, zinssatz, laufzeit, monatliche_rate):
    restschuld = kreditbetrag
    monatliche_tilgungssaetze = []
    jährliche_tilgungssaetze = []

    for jahr in range(1, laufzeit + 1):
        jährliche_tilgung_summe = 0
        for monat in range(12):  # 12 Monate pro Jahr
            zins = restschuld * (zins_pro_jahr / 12)
            tilgung = monatliche_rate - zins
            restschuld -= tilgung
            jährliche_tilgung_summe += tilgung
            if jahr == 1:
                monatliche_tilgungssatz = (tilgung / kreditbetrag) * 100
                monatliche_tilgungssaetze.append(monatliche_tilgungssatz)
        jährliche_tilgungssatz = (jährliche_tilgung_summe / kreditbetrag) * 100
        jährliche_tilgungssaetze.append(jährliche_tilgungssatz)

    return monatliche_tilgungssaetze, jährliche_tilgungssaetze

# Interaktive Eingaben
st.title("📊 Kreditverkaufsrechner")

st.markdown("### Schritt 1: Finanzierungsbedarf eingeben")
kreditbetrag = st.number_input("Finanzierungsbedarf (€):", min_value=2500, max_value=50000, step=100)

if kreditbetrag:
    st.markdown("### Schritt 2: Laufzeit eingeben")
    laufzeit = st.number_input("Gewünschte Laufzeit (in Jahren):", min_value=1, max_value=20, step=1)

if kreditbetrag and laufzeit:
    st.markdown("### Schritt 3: Kapitaldienst eingeben")
    kapitaldienst = st.number_input("Aktueller Kapitaldienst (€):", min_value=0.0, step=50.0)

if kreditbetrag and laufzeit and kapitaldienst:
    st.markdown("### Schritt 4: Wunschrate eingeben")
    wunschrate = st.number_input("Wunschrate (€):", min_value=0.0, step=50.0)

    st.markdown("### Schritt 5: Möchten Sie eine Restkreditversicherung (RKV) hinzufügen?")
    rkv_option = st.radio("RKV-Option:", options=["Ja", "Nein"])

# Berechnung erst starten, wenn alle Eingaben abgeschlossen sind
if kreditbetrag and laufzeit and kapitaldienst and wunschrate and st.button("Berechnung starten"):
    with st.spinner("Berechnung wird durchgeführt..."):
        time.sleep(2)  # Simulierte Ladezeit

    zinssatz = get_interest_rate(kreditbetrag)
    if zinssatz is None:
        st.error("Bitte geben Sie einen Kreditbetrag zwischen 2.500 € und 50.000 € ein.")
    else:
        # Berechnungen
        monatliche_rate = calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit)
        zins_anteile, tilgungs_anteile = calculate_zins_tilgung(kreditbetrag, zinssatz, laufzeit, monatliche_rate)
        monatliche_tilgungssaetze, jährliche_tilgungssaetze = calculate_tilgungssaetze(kreditbetrag, zinssatz, laufzeit, monatliche_rate)

        gesamtzins = sum(zins_anteile)
        gesamtaufwand = gesamtzins + kreditbetrag

        # Ergebnisse übersichtlich darstellen
        st.markdown("## 🏦 Ergebnisse")
        st.markdown(
            f"""
            ### Monatliche Rate (ohne RKV)
            💰 **{monatliche_rate:.2f} €**
            
            ### Monatliche Rate (mit Restkreditversicherung)
            📉 **{monatliche_rate + kreditbetrag * 0.00273:.2f} €**

            ### Zinssatz
            🔍 **{zinssatz * 100:.2f}%**

            ### Tilgungssätze
            📊 **Anfänglicher Tilgungssatz (1. Monat): {monatliche_tilgungssaetze[0]:.2f}%**
            📊 **Tilgungssatz im 1. Jahr: {jährliche_tilgungssaetze[0]:.2f}%**
            📊 **Tilgungssatz im 2. Jahr: {jährliche_tilgungssaetze[1]:.2f}%**
            📊 **Tilgungssatz im 3. Jahr: {jährliche_tilgungssaetze[2]:.2f}%**

            ### Gesamter Zinsaufwand
            📉 **{gesamtzins:,.2f} €**

            ### Gesamtaufwand (Kreditbetrag + Zinsen)
            💸 **{gesamtaufwand:,.2f} €**
            """
        )

        # Visualisierung: Zins- und Tilgungsanteile über die gesamte Laufzeit
        fig, ax = plt.subplots(figsize=(10, 4))
        x = np.arange(1, len(zins_anteile) + 1)  # Gesamte Laufzeit
        ax.bar(x, zins_anteile, label="Zinsen", color="gray", alpha=0.7)
        ax.bar(x, tilgungs_anteile, bottom=zins_anteile, label="Tilgung", color="orange", alpha=0.9)
        ax.set_title("Zins- und Tilgungsanteile über die gesamte Laufzeit", fontsize=14)
        ax.set_xlabel("Monat", fontsize=12)
        ax.set_ylabel("Betrag (€)", fontsize=12)
        ax.legend()
        st.pyplot(fig)










