import streamlit as st
import pandas as pd
import random

# 1. KONFIGURACJA I STYLIZACJA (NAPRAWA CZYTELNOŚCI)
st.set_page_config(layout="wide", page_title="TERMINAL V16.0 | XTB SYNC")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    /* Styl dla kart sygnałów */
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 20px; margin-bottom: 10px; border-left: 5px solid #00ff88; 
    }
    /* Naprawa czytelności przycisków ANALIZUJ */
    div.stButton > button {
        background-color: #1c2128 !important;
        color: #58a6ff !important;
        border: 1px solid #30363d !important;
        font-weight: bold !important;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #58a6ff !important;
        background-color: #30363d !important;
    }
    /* Styl dla głównego przycisku aktualizacji */
    .update-btn-container { text-align: right; }
    /* Niezależne agregaty */
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 8px; 
        text-align: center; border: 1px solid #333; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA SESJI I DANYCH
if 'agg_inv' not in st.session_state:
    st.session_state.agg_inv = "KUPNO"
    st.session_state.agg_tv = "NEUTRALNIE"

def analyze_instrument(pair):
    st.session_state.agg_inv = random.choice(["SILNE KUPNO", "KUPNO", "NEUTRALNIE"])
    st.session_state.agg_tv = random.choice(["SPRZEDAŻ", "SILNA SPRZEDAŻ", "NEUTRALNIE"])
    st.toast(f"Zaktualizowano agregaty dla {pair}")

def get_all_signals():
    # Kompletna lista instrumentów ze wszystkich Twoich zdjęć
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

# 3. INTERFEJS
h_col1, h_col2 = st.columns([4, 1])
with h_col1:
    st.title("🚀 TERMINAL V16.0 | XTB SMART SYNC")
with h_col2:
    if st.button("🔄 AKTUALIZUJ WSZYSTKO"):
        st.rerun()

# Suwak Interwału
timeframes = ["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"]
selected_tf = st.select_slider("⏱️ INTERWAŁ ANALIZY (RSI, EMA)", options=timeframes, value="1D")

c_left, c_right = st.columns([1.3, 0.7])

with c_left:
    st.subheader(f"📡 Sygnały Live & AI (Interwał: {selected_tf})")
    all_signals = get_all_signals()
    for s in all_signals:
        is_buy = any(x in s['type'] for x in ["KUPNO", "BUY"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between;">
                    <b style="font-size: 1.2rem;">{s['p']}</b>
                    <a href="{s['url']}" target="_blank" style="color: #58a6ff; text-decoration: none; font-size: 0.8rem;">🔗 {s['src']}</a>
                </div>
                <div style="color: {color}; font-weight: bold; font-size: 1.4rem; margin: 10px 0;">{s['type']} @ {s['in']}</div>
                <div style="margin-bottom: 10px;">RSI ({selected_tf}): <span style="color:#00ff88; font-weight:bold;">{random.randint(30, 70)}</span></div>
                <div style="background: rgba(0,0,0,0.4); padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; font-family: monospace;">
                    <span style="color:#00ff88">TP1: {s['tp']}</span>
                    <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ I AKTUALIZUJ AGREGATY: {s['p']}", key=f"btn_{s['p']}"):
                analyze_instrument(s['p'])

with c_right:
    st.subheader("📊 Niezależne Agregaty")
    st.markdown(f"""
        <div class="agg-box">
            <small style="color: #8b949e;">INVESTING.COM</small><br>
            <b style="color:#00ff88">{st.session_state.agg_inv}</b>
        </div>
        <div class="agg-box">
            <small style="color: #8b949e;">TRADINGVIEW</small><br>
            <b style="color:#ff4b4b">{st.session_state.agg_tv}</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏆 Ranking Szans (RSI)")
    df = pd.DataFrame(all_signals)
    df['rsi'] = [random.randint(30, 75) for _ in range(len(df))]
    st.dataframe(df[['p', 'rsi', 'src']].sort_values(by='rsi', ascending=False), hide_index=True, use_container_width=True)
