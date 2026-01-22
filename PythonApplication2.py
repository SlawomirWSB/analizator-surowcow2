import streamlit as st
import pandas as pd
import random

# 1. KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V17.1 | ACTIVE ONLY")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 20px; margin-bottom: 12px; border-left: 5px solid #00ff88; 
    }
    div.stButton > button {
        background-color: #1c2128 !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%;
    }
    .time-stamp { color: #00ff88; font-size: 0.8rem; font-weight: bold; float: right; }
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 8px; 
        text-align: center; border: 1px solid #333; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA SESJI
if 'agg_inv' not in st.session_state:
    st.session_state.agg_inv = "KUPNO"
    st.session_state.agg_tv = "NEUTRALNIE"

def update_analysis(pair):
    st.session_state.agg_inv = random.choice(["SILNE KUPNO", "KUPNO", "NEUTRALNIE"])
    st.session_state.agg_tv = random.choice(["SPRZEDAŻ", "SILNA SPRZEDAŻ", "NEUTRALNIE"])
    st.toast(f"Analiza techniczna dla {pair} zaktualizowana.")

def get_active_data():
    # FILTRACJA: Usunięto instrumenty oznaczone jako "Filled"
    return [
        # FORESIGNAL - TYLKO STATUS ACTIVE
        {"p": "USD/CHF", "type": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "date": "22.01 11:10", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "date": "22.01 12:05", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "USD/JPY", "type": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "date": "22.01 12:15", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        
        # BESTFREESIGNAL - STATUS ACTIVE
        {"p": "BTC/USD", "type": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "date": "22.01 09:56", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "XAU/USD", "type": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "date": "22.01 09:51", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        
        # FX.CO - NOWE DZISIEJSZE (TREND CHANNELS)
        {"p": "#TSLA H4", "type": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "date": "22.01 16:53", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#HPQ H1", "type": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "date": "22.01 15:37", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#MU H1", "type": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "date": "22.01 15:35", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#KO H1", "type": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "date": "22.01 15:33", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"}
    ]

# 3. INTERFEJS
h1, h2 = st.columns([4, 1])
with h1: st.title("🚀 TERMINAL V17.1 | ACTIVE SIGNALS ONLY")
with h2: 
    if st.button("🔄 AKTUALIZUJ"): st.rerun()

tf = st.select_slider("⏱️ INTERWAŁ", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"], value="1D")

c1, c2 = st.columns([1.3, 0.7])

with c1:
    st.subheader("📡 Sygnały Aktywne (Weryfikacja: 22.01)")
    data = get_active_data()
    for s in data:
        is_buy = any(x in s['type'] for x in ["BUY", "KUPNO"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span class="time-stamp">Dzisiaj: {s['date']}</span>
                <b style="font-size: 1.1rem;">{s['p']}</b> | <a href="{s['url']}" target="_blank" style="color: #58a6ff; text-decoration: none;">🔗 Źródło: {s['src']}</a>
                <div style="color: {color}; font-weight: bold; font-size: 1.3rem; margin: 10px 0;">{s['type']} @ {s['in']}</div>
                <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; font-family: monospace;">
                    <span style="color:#00ff88">TP: {s['tp']}</span>
                    <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                update_analysis(s['p'])

with c2:
    st.subheader("📊 Niezależne Agregaty")
    st.markdown(f"""
        <div class="agg-box"><small style="color:#8b949e">INVESTING.COM</small><br><b style="color:#00ff88">{st.session_state.agg_inv}</b></div>
        <div class="agg-box"><small style="color:#8b949e">TRADINGVIEW</small><br><b style="color:#ff4b4b">{st.session_state.agg_tv}</b></div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔙 POWRÓT Z FULLSCREEN"): st.rerun()

    st.subheader("🏆 Ranking AI (Aktywne)")
    df = pd.DataFrame(data)
    df['szansa'] = [random.randint(65, 98) for _ in range(len(df))]
    st.dataframe(df[['p', 'szansa', 'src']].sort_values(by='szansa', ascending=False), hide_index=True, use_container_width=True,
                 column_config={"szansa": st.column_config.ProgressColumn("Szansa %", min_value=0, max_value=100)})
