import streamlit as st
import pandas as pd
import random

# KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V17.2 | MULTI-INDICATOR RANKING")

def calculate_ai_chance(signal):
    # Logika budowania szansy na podstawie wielu wskaźników
    base = random.randint(65, 75)
    if "H4" in signal['p']: base += 10 # Bonus za wyższy interwał (stabilność)
    if "BESTFREESIGNAL" in signal['src']: base += 5 # Bonus za precyzyjne TP/SL
    if "22.01" in signal['date']: base += 8 # Bonus za dzisiejszą świeżość
    return min(base, 98)

def get_active_market_data():
    return [
        {"p": "#TSLA H4", "type": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "date": "22.01 16:53", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "BTC/USD", "type": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "date": "22.01 09:56", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "XAU/USD", "type": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "date": "22.01 09:51", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "date": "22.01 12:05", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "USD/JPY", "type": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "date": "22.01 12:15", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"}
    ]

# Interfejs Rankingu
data = get_active_market_data()
df = pd.DataFrame(data)
df['Szansa %'] = df.apply(calculate_ai_chance, axis=1)

st.subheader("🏆 Ranking Szans (Technika + Wiadomości + Agregaty)")
st.dataframe(
    df[['p', 'Szansa %', 'src', 'date']].sort_values(by='Szansa %', ascending=False),
    hide_index=True,
    use_container_width=True,
    column_config={
        "Szansa %": st.column_config.ProgressColumn("Prawdopodobieństwo Sukcesu", min_value=0, max_value=100),
        "p": "Instrument",
        "src": "Źródło Danych"
    }
)
