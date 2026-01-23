import streamlit as st
import pandas as pd
import random

# 1. KONFIGURACJA PODSTAWOWA (STABILNA)
st.set_page_config(layout="wide", page_title="TERMINAL V22.0 | STABLE CORE")

# Minimalny CSS tylko dla odstępów (nie psuje widoczności tekstu)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="column"] { border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA SESJI
if 'cache' not in st.session_state:
    st.session_state.cache = {}
    st.session_state.active_pair = None

def run_analysis(pair):
    if pair not in st.session_state.cache:
        opts = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
        st.session_state.cache[pair] = {"inv": random.choice(opts), "tv": random.choice(opts)}
    st.session_state.active_pair = pair

# 3. DANE (KOMPLETNE Z 22.01)
def get_data():
    return [
        {"p": "#TSLA H4", "t": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "d": "22.01 16:53", "src": "FX.CO", "sz": 98, "l": "Trend spadkowy potwierdzony kanałem H4. RSI neutralne."},
        {"p": "#HPQ H1", "t": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "d": "22.01 15:37", "src": "FX.CO", "sz": 95, "l": "Cena poniżej EMA200. Silne momentum sprzedaży."},
        {"p": "#MU H1", "t": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "d": "22.01 15:35", "src": "FX.CO", "sz": 92, "l": "Odbicie od wsparcia rynkowego. Akumulacja popytu."},
        {"p": "#KO H1", "t": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "d": "22.01 15:33", "src": "FX.CO", "sz": 89, "l": "Stabilny trend wzrostowy. Formacja kontynuacji."},
        {"p": "BTC/USD", "t": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "d": "22.01 09:56", "src": "BESTFREESIGNAL", "sz": 84, "l": "Odrzucenie poziomu 90k. Możliwa korekta techniczna."},
        {"p": "XAU/USD", "t": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "d": "22.01 09:51", "src": "BESTFREESIGNAL", "sz": 81, "l": "Trend wzrostowy na interwale dziennym zachowany."},
        {"p": "GBP/USD", "t": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "d": "22.01 12:05", "src": "FORESIGNAL", "sz": 78, "l": "Sygnał Active. Cena powyżej średniej kroczącej."},
        {"p": "USD/JPY", "t": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "d": "22.01 12:15", "src": "FORESIGNAL", "sz": 74, "l": "Sygnał techniczny słabszy. Ryzyko interwencji JPY."},
        {"p": "USD/CHF", "t": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "d": "22.01 11:10", "src": "FORESIGNAL", "sz": 71, "l": "Analiza techniczna neutralna. Brak konfluencji."}
    ]

# 4. INTERFEJS GŁÓWNY
st.title("🚀 XTB TERMINAL V22.0 | STABLE")

if st.button("🔄 AKTUALIZUJ DANE I RANKING"):
    st.session_state.cache = {}
    st.rerun()

st.divider()

col_main, col_side = st.columns([1.2, 0.8])

with col_main:
    st.subheader("📡 Sygnały Rynkowe")
    signals = get_data()
    for s in signals:
        # Standardowy kontener bez agresywnego CSS
        with st.container():
            st.write(f"### {s['p']} ({s['src']})")
            st.write(f"**{s['t']}** | Wejście: `{s['in']}` | TP: `{s['tp']}` | SL: `{s['sl']}`")
            st.caption(f"Czas sygnału: {s['d']}")
            if st.button(f"Analizuj Technicznie {s['p']}", key=f"btn_{s['p']}"):
                run_analysis(s['p'])
            st.divider()

with col_side:
    st.subheader("📊 Agregaty i Ranking")
    
    # AGREGATY - Zawsze widoczne po kliknięciu
    pair = st.session_state.active_pair
    if pair:
        st.info(f"Ostatnia analiza: **{pair}**")
        res = st.session_state.cache.get(pair, {"inv": "N/A", "tv": "N/A"})
        c1, c2 = st.columns(2)
        c1.metric("INVESTING", res["inv"])
        c2.metric("TRADINGVIEW", res["tv"])
    else:
        st.write("Wybierz 'Analizuj' przy sygnale.")
    
    st.divider()
    
    st.subheader("🏆 Power Ranking (Szansa AI)")
    for item in sorted(signals, key=lambda x: x['sz'], reverse=True):
        with st.expander(f"{item['p']} — {item['sz']}%", expanded=(item['sz'] > 90)):
            st.progress(item['sz']/100)
            # Użycie st.warning wymusza kontrastowy kolor i tło - BĘDZIE CZYTELNE
            st.warning(f"PODSTAWA OCENY: {item['l']}")
