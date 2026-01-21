import streamlit as st
import pandas as pd
from datetime import datetime
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V13.0 | FULL SOURCE SYNC")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    div.stButton > button {
        background: linear-gradient(45deg, #00ff88, #00cc6a) !important;
        color: #000 !important; font-weight: 900 !important; border-radius: 8px !important; height: 50px;
    }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; margin-bottom: 15px; border-left: 5px solid #00ff88; 
    }
    .rsi-val { color: #00ff88; font-weight: bold; background: rgba(0,255,136,0.1); padding: 2px 5px; border-radius: 4px; }
    .source-tag { font-size: 0.7rem; border: 1px solid #444; padding: 2px 6px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# 2. SILNIK INTEGRACJI DANYCH (SYNC ZE ZDJĘCIAMI)
def fetch_all_synced_signals():
    # Dane precyzyjnie odwzorowane z Twoich załączników
    return [
        # Źródło: BESTFREESIGNAL
        {
            "p": "XAU/USD", "type": "KUPNO", "in": "4,860.000", "tp": "4,863.770", 
            "sl": "4,849.770", "date": "2026-01-21 15:48:22", "src": "BESTFREESIGNAL", "rsi": 36, "score": 91
        },
        # Źródło: DAILYFOREX
        {
            "p": "EUR/USD", "type": "SPRZEDAŻ", "in": "1.180", "tp": "1.158", 
            "sl": "1.188", "date": "2026-01-21 14:55:00", "src": "DAILYFOREX", "rsi": 44, "score": 82
        },
        {
            "p": "EUR/JPY", "type": "SPRZEDAŻ", "in": "185.500", "tp": "180.000", 
            "sl": "187.000", "date": "2026-01-20 13:49:00", "src": "DAILYFOREX", "rsi": 49, "score": 78
        },
        # Źródło: FORESIGNAL
        {
            "p": "NZD/USD", "type": "SPRZEDAŻ", "in": "0.5845", "tp": "0.5837", 
            "sl": "0.5855", "date": "2026-01-21 19:25:00", "src": "FORESIGNAL", "rsi": 38, "score": 89
        },
        {
            "p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", 
            "sl": "1.3411", "date": "2026-01-21 17:07:00", "src": "FORESIGNAL", "rsi": 52, "score": 85
        },
        # Źródło: FX.CO
        {
            "p": "#ORCL H1", "type": "BUY STOP", "in": "172.6500", "tp": "182.7210", 
            "sl": "170.5966", "date": "2026-01-21 19:29:00", "src": "FX.CO", "rsi": 55, "score": 93
        },
        {
            "p": "#CVX H1", "type": "SELL STOP", "in": "165.1300", "tp": "149.6100", 
            "sl": "169.4000", "date": "2026-01-21 16:30:00", "src": "FX.CO", "rsi": 32, "score": 87
        }
    ]

# 3. INTERFEJS GŁÓWNY
st.title("🚀 TERMINAL V13.0 | ALL-IN-ONE SYNC")

if st.button("🔄 AKTUALIZUJ WSZYSTKIE ŹRÓDŁA (4 SYNC)"):
    st.session_state.all_signals = fetch_all_synced_signals()

if 'all_signals' not in st.session_state:
    st.session_state.all_signals = fetch_all_synced_signals()

col_main, col_stats = st.columns([1.3, 0.7])

with col_main:
    st.subheader("📡 Zagregowany Live Feed")
    for s in st.session_state.all_signals:
        # Kolorystyka zależna od typu transakcji
        is_buy = any(x in s['type'] for x in ["KUPNO", "BUY"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        
        st.markdown(f"""
        <div class="signal-card" style="border-left-color: {color}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <b style="font-size: 1.1rem;">{s['p']}</b>
                <span class="source-tag">{s['src']}</span>
            </div>
            <div style="font-size: 1.3rem; color: {color}; font-weight: bold;">
                {s['type']} @ {s['in']}
            </div>
            <div style="margin: 10px 0; font-size: 0.9rem; color: #8b949e;">
                Data: {s['date']} | RSI: <span class="rsi-val">{s['rsi']}</span>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; font-family: monospace;">
                <span style="color:#00ff88">TP1: {s['tp']}</span>
                <span style="color:#ff4b4b">SL: {s['sl']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_stats:
    st.subheader("🏆 Ranking Skuteczności")
    df = pd.DataFrame(st.session_state.all_signals).sort_values(by="score", ascending=False)
    st.dataframe(
        df[['p', 'type', 'src', 'score']], 
        hide_index=True, 
        use_container_width=True
    )
    
    st.markdown("---")
    st.subheader("📊 Podsumowanie Rynku")
    ac1, ac2 = st.columns(2)
    with ac1:
        st.metric("Aktywne Sygnały", len(st.session_state.all_signals))
    with ac2:
        buy_count = len([x for x in st.session_state.all_signals if "BUY" in x['type'] or "KUPNO" in x['type']])
        st.metric("Nastawienie (BUY)", f"{int(buy_count/len(st.session_state.all_signals)*100)}%")
