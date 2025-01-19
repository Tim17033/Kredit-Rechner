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

    st.markdown("### Schritt 5: Möchten Sie eine Ratenkreditversicherung (RKV) hinzufügen?")
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
        zins_anteil = kreditbetrag * (zinssatz / 12)
        tilgung_anteil = monatliche_rate - zins_anteil
        anfaenglicher_tilgungsprozentsatz = (tilgung_anteil / kreditbetrag) * 100
        zinsprozentsatz = zinssatz * 100

        # Kapitaldienstprüfung
        if monatliche_rate > kapitaldienst:
            laufzeit += 1
            monatliche_rate = calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit)
            st.warning(f"Die gewünschte Rate passt nicht in den aktuellen Kapitaldienst. Laufzeit wurde auf **{laufzeit} Jahre** angepasst!")

        # Wunschrate-Abgleich
        if monatliche_rate < wunschrate:
            differenz = wunschrate - monatliche_rate
            st.info(f"Deine Wunschrate ist **{differenz:.2f} €** unter der tatsächlichen Rate. Wow, wie cool! 🚀")

        # RKV-Berechnung
        rkv_aufschlag = kreditbetrag * 0.00273
        monatliche_rate_mit_rkv = monatliche_rate + rkv_aufschlag

        # Berechnung der Zins- und Tilgungsanteile
        zins_anteile, tilgungs_anteile = calculate_zins_tilgung(kreditbetrag, zinssatz, laufzeit, monatliche_rate)

        # Gesamtzinsberechnung
        gesamtzins = sum(zins_anteile)
        gesamtaufwand = gesamtzins + kreditbetrag

        # Besondere Hervorhebung der Ergebnisse
        st.markdown(
            f"""
            ## 🏦 Ergebnisse
            - 💰 **Monatliche Rate (ohne RKV): {monatliche_rate:.2f} €**
            - 📉 **Monatliche Rate (mit RKV): {monatliche_rate_mit_rkv:.2f} €**
            - 🔍 **Anfänglicher Zinssatz: {zinsprozentsatz:.2f}%**
            - 📊 **Anfänglicher Tilgungssatz: {anfaenglicher_tilgungsprozentsatz:.2f}%**
            - 📉 **Gesamter Zinsaufwand über die Laufzeit: {gesamtzins:,.2f} €**
            - 💸 **Gesamtaufwand (Kreditbetrag + Zinsen): {gesamtaufwand:,.2f} €**
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








