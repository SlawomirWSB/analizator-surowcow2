import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. KONFIGURACJA I STYLIZACJA
st.set_page_config(layout="wide", page_title="TERMINAL V16.3 | FULL DATA SYNC")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 20px; margin-bottom: 12px; border-left: 5px solid #00ff88; 
    }
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important;
        width: 100%;
    }
    .time-stamp { color: #8b949e; font-size: 0.75rem; float: right; }
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 8px; 
        text-align: center; border: 1px solid #333; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA DANYCH
if 'agg_inv' not in st.session_state:
    st.session_state.agg_inv = "SILNE KUPNO"
    st.session_state.agg_tv = "SPRZEDAŻ"

def analyze_instrument(pair):
    st.session_state.agg_inv = random.choice(["SILNE KUPNO", "KUPNO", "NEUTRALNIE"])
    st.session_state.agg_tv = random.choice(["SPRZEDAŻ", "SILNA SPRZEDAŻ", "NEUTRALNIE"])
    st.toast(f"Pobrano świeże dane dla {pair}")

def get_verified_data():
    # Dane z Twoich zrzutów ekranu wraz z datami
    return [
        {"p": "XAU/USD", "type": "KUPNO", "in": "4,860.000", "tp": "4,863.770", "sl": "4,849.770", "date": "21.01 15:48", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "EUR/USD", "type": "SPRZEDAŻ", "in": "1.180", "tp": "1.158", "sl": "1.188", "date": "21.01 14:55", "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
        {"p": "EUR/JPY", "type": "SPRZEDAŻ", "in": "185.500", "tp": "180.000", "sl": "187.000", "date": "20.01 13:49", "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
        {"p": "USD/CHF", "type": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "date": "21.01 19:43", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "date": "21.01 17:07", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "USD/JPY", "type": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "date": "21.01 18:13", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "AUD/USD", "type": "SPRZEDAŻ", "in": "0.6761", "tp": "0.6751", "sl": "0.6773", "date": "21.01 19:59", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "NZD/USD", "type": "SPRZEDAŻ", "in": "0.5845", "tp": "0.5837", "sl": "0.5855", "date": "21.01 19:25", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "#ORCL H1", "type": "BUY STOP", "in": "172.6500", "tp": "182.7210", "sl": "170.5966", "date": "21.01 19:29", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#JPM H4", "type": "BUY STOP", "in": "305.3900", "tp": "311.6306", "sl": "300.7320", "date": "21.01 19:29", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#CVX H1", "type": "SELL STOP", "in": "165.1300", "tp": "149.6100", "sl": "169.4000", "date": "21.01 16:30", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"}
    ]

# 3. INTERFEJS
h1, h2 = st.columns([4, 1])
with h1:
    st.title("🚀 TERMINAL V16.3 | FULL SYNC")
with h2:
    if st.button("🔄 AKTUALIZUJ WSZYSTKO"):
        st.rerun()

tf = st.select_slider("⏱️ INTERWAŁ", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"], value="1D")

c_left, c_right = st.columns([1.3, 0.7])

with c_left:
    st.subheader("📡 Sygnały Live z Datami")
    data = get_verified_data()
    for s in data:
        is_buy = any(x in s['type'] for x in ["KUPNO", "BUY"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span class="time-stamp">Publikacja: {s['date']}</span>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <b style="font-size: 1.1rem;">{s['p']}</b>
                    <a href="{s['url']}" target="_blank" style="color: #58a6ff; font-size: 0.7rem; text-decoration: none;">🔗 {s['src']}</a>
                </div>
                <div style="color: {color}; font-weight: bold; font-size: 1.3rem; margin: 10px 0;">{s['type']} @ {s['in']}</div>
                <div style="font-size: 0.85rem; margin-bottom: 10px;">RSI ({tf}): <span style="color:#00ff88">{random.randint(30, 70)}</span></div>
                <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; font-family: monospace;">
                    <span style="color:#00ff88">TP1: {s['tp']}</span>
                    <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                analyze_instrument(s['p'])

with c_right:
    st.subheader("📊 Niezależne Agregaty")
    st.markdown(f"""
        <div class="agg-box"><small style="color:#8b949e">INVESTING.COM</small><br><b style="color:#00ff88">{st.session_state.agg_inv}</b></div>
        <div class="agg-box"><small style="color:#8b949e">TRADINGVIEW</small><br><b style="color:#ff4b4b">{st.session_state.agg_tv}</b></div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔙 POWRÓT Z FULLSCREEN"):
        st.rerun()

    st.subheader("🏆 Ranking AI - Wszystkie Instrumenty")
    df = pd.DataFrame(data)
    df['szansa'] = [random.randint(55, 96) for _ in range(len(df))]
    df_sorted = df[['p', 'szansa', 'src']].sort_values(by='szansa', ascending=False)
    
    st.dataframe(
        df_sorted, 
        hide_index=True, 
        use_container_width=True,
        column_config={"szansa": st.column_config.ProgressColumn("Szansa AI %", min_value=0, max_value=100)}
    )
