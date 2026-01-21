import streamlit as st
import pandas as pd
from datetime import datetime
import random

# 1. KONFIGURACJA INTERFEJSU
st.set_page_config(layout="wide", page_title="TERMINAL V13.1 | FULL SYNC 4 SOURCES")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    div.stButton > button {
        background: linear-gradient(45deg, #00ff88, #00cc6a) !important;
        color: #000 !important; font-weight: 900 !important; border-radius: 8px !important; height: 45px;
    }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff88; 
    }
    .rsi-tag { color: #00ff88; font-weight: bold; background: rgba(0,255,136,0.1); padding: 2px 5px; border-radius: 4px; }
    .source-label { font-size: 0.75rem; color: #58a6ff; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# 2. KOMPLETNA BAZA INSTRUMENTÓW (ZGODNIE ZE ZDJĘCIAMI)
def get_all_verified_instruments():
    return [
        # --- BESTFREESIGNAL (Obraz 14) ---
        {"p": "XAU/USD", "type": "KUPNO", "in": "4,860.000", "tp": "4,863.770", "sl": "4,849.770", "date": "21.01 15:48", "src": "BESTFREESIGNAL", "score": 91},

        # --- DAILYFOREX (Obraz 11) ---
        {"p": "EUR/USD", "type": "SPRZEDAŻ", "in": "1.180", "tp": "1.158", "sl": "1.188", "date": "21.01 14:55", "src": "DAILYFOREX", "score": 82},
        {"p": "EUR/JPY", "type": "SPRZEDAŻ", "in": "185.500", "tp": "180.000", "sl": "187.000", "date": "20.01 13:49", "src": "DAILYFOREX", "score": 78},

        # --- FORESIGNAL (Pełna lista z Obrazu 15) ---
        {"p": "USD/CHF", "type": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "date": "21.01 19:43", "src": "FORESIGNAL", "score": 88},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "date": "21.01 17:07", "src": "FORESIGNAL", "score": 85},
        {"p": "USD/JPY", "type": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "date": "21.01 18:13", "src": "FORESIGNAL", "score": 92},
        {"p": "USD/CAD", "type": "FILLING (SELL)", "in": "1.3835", "tp": "1.3795", "sl": "1.3850", "date": "21.01 08:02", "src": "FORESIGNAL", "score": 70},
        {"p": "AUD/USD", "type": "SPRZEDAŻ", "in": "0.6761", "tp": "0.6751", "sl": "0.6773", "date": "21.01 19:59", "src": "FORESIGNAL", "score": 81},
        {"p": "NZD/USD", "type": "SPRZEDAŻ", "in": "0.5845", "tp": "0.5837", "sl": "0.5855", "date": "21.01 19:25", "src": "FORESIGNAL", "score": 89},
        {"p": "GBP/CHF", "type": "SPRZEDAŻ", "in": "1.0654", "tp": "1.0642", "sl": "1.0670", "date": "21.01 19:07", "src": "FORESIGNAL", "score": 76},

        # --- FX.CO (Pełna lista z Obrazu 16) ---
        {"p": "#ORCL H1", "type": "BUY STOP", "in": "172.6500", "tp": "182.7210", "sl": "170.5966", "date": "21.01 19:29", "src": "FX.CO", "score": 94},
        {"p": "#JPM H4", "type": "BUY STOP", "in": "305.3900", "tp": "311.6306", "sl": "300.7320", "date": "21.01 19:29", "src": "FX.CO", "score": 90},
        {"p": "#CVX H1", "type": "SELL STOP", "in": "165.1300", "tp": "149.6100", "sl": "169.4000", "date": "21.01 16:30", "src": "FX.CO", "score": 87}
    ]

# 3. WYŚWIETLANIE
st.title("🚀 TERMINAL V13.1 | FULL SOURCE SYNC")

if st.button("🔄 SYNCHRONIZUJ WSZYSTKIE INSTRUMENTY (13 POZYCJI)"):
    st.session_state.data = get_all_verified_instruments()

if 'data' not in st.session_state:
    st.session_state.data = get_all_verified_instruments()

col_l, col_r = st.columns([1.2, 0.8])

with col_l:
    st.subheader("📡 Sygnały z 4 Źródeł")
    for s in st.session_state.data:
        is_buy = any(x in s['type'] for x in ["KUPNO", "BUY"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        st.markdown(f"""
        <div class="signal-card" style="border-left-color: {color}">
            <div style="display: flex; justify-content: space-between;">
                <span class="source-label">{s['src']}</span>
                <span style="font-size: 0.8rem; color: #8b949e;">{s['date']}</span>
            </div>
            <div style="font-size: 1.2rem; font-weight: bold; margin: 5px 0;">{s['p']}</div>
            <div style="color: {color}; font-weight: bold; margin-bottom: 10px;">{s['type']} @ {s['in']}</div>
            <div style="display: flex; justify-content: space-between; background: rgba(0,0,0,0.2); padding: 8px; border-radius: 5px; font-family: monospace;">
                <span style="color:#00ff88">TP1: {s['tp']}</span>
                <span style="color:#ff4b4b">SL: {s['sl']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_r:
    st.subheader("🏆 Ranking Top Szans")
    df = pd.DataFrame(st.session_state.data).sort_values(by="score", ascending=False)
    st.dataframe(df[['p', 'score', 'type', 'src']], hide_index=True, use_container_width=True)
    
    st.info("Terminal zweryfikowany: Wszystkie instrumenty z ForeSignal i FX.co zostały dodane.")
