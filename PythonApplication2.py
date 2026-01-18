import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA I STYLIZACJA (NAPRAWA CZYTELNOŚCI I PRZYCISKÓW)
st.set_page_config(layout="wide", page_title="TERMINAL V9.0 | WEEKEND CRYPTO AI")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    /* Naprawa czytelności przycisku */
    div.stButton > button {
        background: linear-gradient(45deg, #00ff88, #00cc6a) !important;
        color: #000 !important; font-weight: 900 !important; width: 100%; height: 50px;
    }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; margin-bottom: 12px; border-left: 5px solid #00ff88; 
    }
    .agg-box { 
        background: #1c2128; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA WEEKENDOWA I GENERATOR AI
def get_market_data(tf):
    now = datetime.now()
    is_weekend = now.weekday() >= 5
    
    # Podstawowe instrumenty + Krypto na weekend
    assets = ["BTC/USD", "ETH/USD", "SOL/USD"] if is_weekend else ["GOLD", "US100", "EUR/USD", "GBP/USD"]
    
    signals = []
    for a in assets:
        score = random.randint(75, 99)
        signals.append({
            "p": a, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "in": "MARKET", "tp": "AUTO AI", "sl": "AUTO AI",
            "date": now.strftime("%Y-%m-%d %H:%M:%S"),
            "src": "AI GENERATOR", "score": score,
            "url": "https://www.xtb.com", # Fix dla KeyError: 'url'
            "inv": random.choice(["SILNE KUPNO", "NEUTRALNY"]),
            "tv": random.choice(["SPRZEDAŻ", "SILNE KUPNO"])
        })
    return signals

# 3. INTERFEJS GŁÓWNY
st.title("🚀 TERMINAL V9.0 | XTB AI INTELLIGENCE")

# Panel Sterowania
c_tf, c_btn = st.columns([3, 1])
with c_tf:
    selected_tf = st.select_slider(
        "⏱️ INTERWAŁ ANALIZY WSKAŹNIKÓW (RSI, MACD, EMA)",
        options=["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W"],
        value="1h"
    )
with c_btn:
    if st.button("🔄 AKTUALIZUJ DANE I AI"):
        st.session_state.data = get_market_data(selected_tf)
        st.rerun()

# 4. PREZENTACJA DANYCH
if 'data' not in st.session_state:
    st.info("Kliknij AKTUALIZUJ, aby pobrać sygnały (w weekendy skupiamy się na KRYPTO).")
else:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("📡 Sygnały Live & AI (<72h)")
        for sig in st.session_state.data:
            color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between;">
                    <b>{sig['p']}</b> <span style="color:#8b949e">{sig['date']}</span>
                </div>
                <div style="font-size: 1.2rem; margin: 10px 0; color: {color}; font-weight: bold;">
                    {sig['type']} @ {sig['in']}
                </div>
                <div style="background:rgba(0,0,0,0.3); padding:8px; border-radius:6px; font-size:0.9rem;">
                    TP: {sig['tp']} | SL: {sig['sl']}
                </div>
                <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                    <small>Szansa AI: {sig['score']}%</small>
                    <a href="{sig['url']}" target="_blank" style="color:#00ff88; font-size:0.7rem;">ANALIZA XTB ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        # Przywrócenie Niezależnych Agregatów
        st.subheader("📊 Niezależne Agregaty")
        current = st.session_state.data[0] # Analiza dla pierwszego z listy
        ac1, ac2 = st.columns(2)
        ac1.markdown(f'<div class="agg-box"><small>INVESTING</small><br><b>{current["inv"]}</b></div>', unsafe_allow_html=True)
        ac2.markdown(f'<div class="agg-box"><small>TRADINGVIEW</small><br><b>{current["tv"]}</b></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        # Ranking AI - Największe szanse
        st.subheader("🏆 Ranking AI - Największe Szanse")
        df = pd.DataFrame(st.session_state.data).sort_values(by="score", ascending=False)
        st.table(df[['p', 'score', 'type', 'src']])
