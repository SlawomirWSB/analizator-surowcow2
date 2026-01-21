import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. KONFIGURACJA I STYLE
st.set_page_config(layout="wide", page_title="TERMINAL V14.0 | XTB SMART SYNC")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; margin-bottom: 15px; border-left: 5px solid #00ff88; 
    }
    .agg-box { 
        background: #1c2128; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #333; margin-bottom: 10px;
    }
    .rsi-badge { 
        background: rgba(0, 255, 136, 0.1); color: #00ff88; padding: 2px 8px; border-radius: 4px; font-weight: bold; 
    }
    .source-link { color: #58a6ff; text-decoration: none; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA GENEROWANIA DANYCH
def get_rsi(pair, timeframe):
    # Symulacja zmiany RSI na podstawie interwału
    seed = sum(ord(c) for c in pair) + len(timeframe)
    random.seed(seed)
    return random.randint(30, 70)

def fetch_data():
    return [
        {"p": "XAU/USD", "type": "KUPNO", "in": "4,860.000", "tp": "4,863.770", "sl": "4,849.770", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "EUR/USD", "type": "SPRZEDAŻ", "in": "1.180", "tp": "1.158", "sl": "1.188", "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
        {"p": "EUR/JPY", "type": "SPRZEDAŻ", "in": "185.500", "tp": "180.000", "sl": "187.000", "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
        {"p": "USD/CHF", "type": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "USD/JPY", "type": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "AUD/USD", "type": "SPRZEDAŻ", "in": "0.6761", "tp": "0.6751", "sl": "0.6773", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "NZD/USD", "type": "SPRZEDAŻ", "in": "0.5845", "tp": "0.5837", "sl": "0.5855", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "#ORCL H1", "type": "BUY STOP", "in": "172.6500", "tp": "182.7210", "sl": "170.5966", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#JPM H4", "type": "BUY STOP", "in": "305.3900", "tp": "311.6306", "sl": "300.7320", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#CVX H1", "type": "SELL STOP", "in": "165.1300", "tp": "149.6100", "sl": "169.4000", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"}
    ]

# 3. INTERFEJS UŻYTKOWNIKA
st.title("🚀 TERMINAL V14.0 | XTB SMART ANALYSIS")

# Suwak Interwału
t_options = ["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"]
selected_tf = st.select_slider("⏱️ WYBIERZ INTERWAŁ ANALIZY WSKAŹNIKÓW (RSI, EMA)", options=t_options, value="1D")

col_left, col_right = st.columns([1.3, 0.7])

with col_left:
    st.subheader(f"📡 Sygnały Live (Interwał: {selected_tf})")
    signals = fetch_data()
    
    for s in signals:
        is_buy = any(x in s['type'] for x in ["KUPNO", "BUY"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        current_rsi = get_rsi(s['p'], selected_tf) # RSI zależne od suwaka
        
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="font-size: 1.1rem;">{s['p']}</b>
                    <a href="{s['url']}" target="_blank" class="source-link">🔗 {s['src']}</a>
                </div>
                <div style="color: {color}; font-weight: bold; font-size: 1.2rem; margin: 8px 0;">
                    {s['type']} @ {s['in']}
                </div>
                <div style="margin-bottom: 10px; font-size: 0.9rem;">
                    RSI ({selected_tf}): <span class="rsi-badge">{current_rsi}</span>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; font-family: monospace;">
                    <span style="color:#00ff88">TP1: {s['tp']}</span>
                    <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=s['p']):
                st.toast(f"Aktualizacja danych dla {s['p']} ({selected_tf})...")

with col_right:
    # Niezależne Agregaty po prawej
    st.subheader("📊 Niezależne Agregaty")
    st.markdown('<div class="agg-box"><small>INVESTING.COM</small><br><b style="color:#00ff88">SILNE KUPNO</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:#ff4b4b">SPRZEDAŻ</b></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏆 Największe Szanse")
    df = pd.DataFrame(signals)
    df['rsi'] = [get_rsi(p, selected_tf) for p in df['p']]
    st.dataframe(df[['p', 'rsi', 'src']].sort_values(by='rsi', ascending=False), hide_index=True)
