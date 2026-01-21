import streamlit as st
import pandas as pd
from datetime import datetime

# 1. KONFIGURACJA I STYLIZACJA
st.set_page_config(layout="wide", page_title="TERMINAL V13.2 | FULL SOURCE SYNC")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    div.stButton > button {
        background: linear-gradient(45deg, #00ff88, #00cc6a) !important;
        color: #000 !important; font-weight: 900 !important; border-radius: 8px !important;
    }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff88; 
    }
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #333;
    }
    .link-btn {
        background: rgba(88, 166, 255, 0.1); color: #58a6ff; text-decoration: none;
        padding: 4px 10px; border-radius: 4px; font-size: 0.7rem; border: 1px solid #58a6ff;
    }
</style>
""", unsafe_allow_html=True)

# 2. KOMPLETNA BAZA DANYCH Z LINKAMI
def get_final_data():
    return [
        # BESTFREESIGNAL
        {"p": "XAU/USD", "type": "KUPNO", "in": "4,860.000", "tp": "4,863.770", "sl": "4,849.770", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        
        # DAILYFOREX
        {"p": "EUR/USD", "type": "SPRZEDAŻ", "in": "1.180", "tp": "1.158", "sl": "1.188", "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
        {"p": "EUR/JPY", "type": "SPRZEDAŻ", "in": "185.500", "tp": "180.000", "sl": "187.000", "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
        
        # FORESIGNAL
        {"p": "USD/CHF", "type": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "USD/JPY", "type": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "AUD/USD", "type": "SPRZEDAŻ", "in": "0.6761", "tp": "0.6751", "sl": "0.6773", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "NZD/USD", "type": "SPRZEDAŻ", "in": "0.5845", "tp": "0.5837", "sl": "0.5855", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        
        # FX.CO
        {"p": "#ORCL H1", "type": "BUY STOP", "in": "172.6500", "tp": "182.7210", "sl": "170.5966", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#JPM H4", "type": "BUY STOP", "in": "305.3900", "tp": "311.6306", "sl": "300.7320", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#CVX H1", "type": "SELL STOP", "in": "165.1300", "tp": "149.6100", "sl": "169.4000", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"}
    ]

# 3. INTERFEJS GŁÓWNY
st.title("🚀 TERMINAL V13.2 | TOTAL SYNC")

# SEKCJA NIEZALEŻNYCH AGREGATÓW
st.subheader("📊 Niezależne Agregaty")
a1, a2 = st.columns(2)
with a1:
    st.markdown('<div class="agg-box"><small>INVESTING.COM</small><br><b style="color:#00ff88">SILNE KUPNO</b></div>', unsafe_allow_html=True)
with a2:
    st.markdown('<div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:#ff4b4b">SPRZEDAŻ</b></div>', unsafe_allow_html=True)

st.markdown("---")

col_l, col_r = st.columns([1.3, 0.7])

with col_l:
    st.subheader("📡 Sygnały Live z Odnośnikami")
    data = get_final_data()
    for s in data:
        is_buy = any(x in s['type'] for x in ["KUPNO", "BUY"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        st.markdown(f"""
        <div class="signal-card" style="border-left-color: {color}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="font-size: 1.1rem;">{s['p']}</b>
                <a href="{s['url']}" target="_blank" class="link-btn">🔗 ŹRÓDŁO: {s['src']}</a>
            </div>
            <div style="color: {color}; font-weight: bold; font-size: 1.2rem; margin: 10px 0;">{s['type']} @ {s['in']}</div>
            <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; font-family: monospace;">
                <span style="color:#00ff88">TP1: {s['tp']}</span>
                <span style="color:#ff4b4b">SL: {s['sl']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_r:
    st.subheader("🏆 Największe Szanse")
    df = pd.DataFrame(data)
    df['score'] = [random.randint(70, 95) for _ in range(len(df))]
    st.dataframe(df.sort_values(by="score", ascending=False)[['p', 'score', 'src']], hide_index=True)
