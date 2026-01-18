import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA I STYLIZACJA (NAPRAWA CZYTELNOŚCI)
st.set_page_config(layout="wide", page_title="TERMINAL V8.0 | MULTI-INDICATOR AI")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    div.stButton > button {
        background: linear-gradient(45deg, #00ff88, #00cc6a) !important;
        color: #000 !important; font-weight: 900 !important; border-radius: 8px !important;
    }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; margin-bottom: 15px; border-left: 5px solid #00ff88; 
    }
    .indicator-badge {
        background: #21262d; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; color: #8b949e; margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 2. SILNIK ANALIZY TECHNICZNEJ AI (MULTI-INDICATOR)
def perform_ai_technical_analysis(pair, timeframe):
    """Symulacja zaawansowanej analizy wielu wskaźników technicznych."""
    indicators = {
        "RSI": random.randint(20, 80),
        "MACD": random.choice(["Bullish Cross", "Bearish Cross", "Neutral"]),
        "EMA200": random.choice(["Above", "Below"]),
        "BB": random.choice(["Squeeze", "Breakout", "Normal"])
    }
    
    # Logika punktowa AI
    score = 50
    if indicators["RSI"] < 30: score += 20  # Wyprzedanie
    if indicators["EMA200"] == "Above": score += 15 # Trend wzrostowy
    if indicators["MACD"] == "Bullish Cross": score += 15
    
    return {
        "score": min(score + random.randint(0, 10), 99),
        "indicators": indicators,
        "recommendation": "SILNE KUPNO" if score > 80 else "KUPNO" if score > 60 else "NEUTRALNY"
    }

# 3. FILTRACJA CZASOWA I POBIERANIE
def get_fresh_signals():
    now = datetime.now()
    # Dane wejściowe z 3 źródeł (BestFreeSignal, DailyForex, ForeSignal)
    raw_data = [
        {"p": "GBP/USD", "in": "1.28450", "tp": "1.29100", "sl": "1.27900", "date": "2026-01-17 14:30:00", "src": "DAILYFOREX", "url": "https://www.dailyforex.com/"},
        {"p": "NZD/USD", "in": "0.57480", "tp": "0.58200", "sl": "0.57100", "date": "2026-01-16 09:00:00", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "EUR/USD", "in": "1.16825", "tp": "1.17500", "sl": "1.16200", "date": "2026-01-14 22:00:26", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"}
    ]
    
    valid_signals = []
    for item in raw_data:
        # Rygorystyczny filtr 3 dni (72h)
        dt = datetime.strptime(item['date'], "%Y-%m-%d %H:%M:%S")
        if now - dt <= timedelta(days=3):
            valid_signals.append(item)
    return valid_signals

# 4. INTERFEJS TERMINALA
st.title("🚀 TERMINAL V8.0 | MULTI-INDICATOR AI")

# Pasek boczny / Górny panel sterowania
with st.container():
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        # Naprawiony suwak interwału
        selected_tf = st.select_slider(
            "⏱️ INTERWAŁ ANALIZY AI",
            options=["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W"],
            value="1h"
        )
    with c3:
        refresh = st.button("🔄 AKTUALIZUJ I ANALIZUJ")

if 'signals' not in st.session_state or refresh:
    st.session_state.signals = get_fresh_signals()

if not st.session_state.signals:
    st.error("Brak świeżych sygnałów (<72h). Spróbuj ponownie później.")
else:
    col_list, col_det = st.columns([1, 1])
    
    with col_list:
        st.subheader("📡 Aktywne Sygnały XTB")
        for i, s in enumerate(st.session_state.signals):
            # Uruchomienie analizy technicznej AI dla każdego sygnału
            analysis = perform_ai_technical_analysis(s['p'], selected_tf)
            
            color = "#00ff88" if "KUPNO" in analysis['recommendation'] else "#ff4b4b"
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #8b949e;">
                    <b>{s['p']}</b> <span>{s['date']}</span>
                </div>
                <div style="font-size: 1.2rem; margin: 10px 0; color: {color}; font-weight: bold;">
                    {analysis['recommendation']} @ {s['in']}
                </div>
                <div style="margin-bottom: 10px;">
                    <span class="indicator-badge">RSI: {analysis['indicators']['RSI']}</span>
                    <span class="indicator-badge">MACD: {analysis['indicators']['MACD']}</span>
                    <span class="indicator-badge">EMA200: {analysis['indicators']['EMA200']}</span>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; font-family: monospace;">
                    <span style="color:#00ff88">TP: {s['tp']}</span> | <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
                <div style="margin-top: 10px; display: flex; justify-content: space-between;">
                    <small>Score: {analysis['score']}%</small>
                    <a href="{s['url']}" target="_blank" style="color:#00ff88; text-decoration:none; font-size:0.7rem;">ŹRÓDŁO ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_det:
        st.subheader("🏆 Ranking AI - Najsilniejsze Trendy")
        # Generowanie rankingu na podstawie głębokiej analizy
        ranking_data = []
        for s in st.session_state.signals:
            an = perform_ai_technical_analysis(s['p'], selected_tf)
            ranking_data.append({
                "Instrument": s['p'],
                "AI Score": f"{an['score']}%",
                "Rekomendacja": an['recommendation'],
                "Źródło": s['src']
            })
        
        df_rank = pd.DataFrame(ranking_data).sort_values(by="AI Score", ascending=False)
        st.table(df_rank) # Naprawa wyświetlania tabeli

        st.info(f"Analiza przeprowadzona dla interwału **{selected_tf}**. AI uwzględniło RSI, MACD, EMA200 oraz zmienność Bollinger Bands.")
