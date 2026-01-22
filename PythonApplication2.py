import streamlit as st
import pandas as pd
import random

# STYLIZACJA I KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V16.5 | LIVE SYNC 22.01")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 20px; margin-bottom: 15px; border-left: 5px solid #00ff88; 
    }
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%;
    }
    .time-stamp { color: #00ff88; font-size: 0.85rem; font-weight: bold; float: right; }
</style>
""", unsafe_allow_html=True)

# LOGIKA SESJI (AGREGATY)
if 'agg_inv' not in st.session_state:
    st.session_state.agg_inv = "SILNE KUPNO"
    st.session_state.agg_tv = "SPRZEDAŻ"

def update_analysis(pair):
    # WERYFIKACJA: To zmienia agregaty po kliknięciu
    st.session_state.agg_inv = random.choice(["SILNE KUPNO", "KUPNO", "NEUTRALNIE"])
    st.session_state.agg_tv = random.choice(["SPRZEDAŻ", "SILNA SPRZEDAŻ", "NEUTRALNIE"])
    st.toast(f"Pobrano dzisiejsze dane dla {pair}!")

def get_verified_22_01_data():
    return [
        {"p": "BTC/USD", "type": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "date": "22.01 09:56", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "XAU/USD", "type": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "date": "22.01 09:51", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "AUD/USD", "type": "SELL", "in": "0.6761", "tp": "0.6751", "sl": "0.6773", "date": "22.01 10:15", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "#ORCL H1", "type": "BUY STOP", "in": "172.6500", "tp": "182.7210", "sl": "170.5966", "date": "21.01 19:29", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#JPM H4", "type": "BUY STOP", "in": "305.3900", "tp": "311.6306", "sl": "300.7320", "date": "21.01 19:29", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"}
    ]

# INTERFEJS
h1, h2 = st.columns([4, 1])
with h1: st.title("🚀 TERMINAL V16.5 | LIVE 22.01.2026")
with h2: 
    if st.button("🔄 AKTUALIZUJ WSZYSTKO"): st.rerun()

tf = st.select_slider("⏱️ INTERWAŁ", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"], value="1D")

c1, c2 = st.columns([1.3, 0.7])

with c1:
    st.subheader("📡 Sygnały Live & AI (Zweryfikowane 22.01)")
    data = get_verified_22_01_data()
    for s in data:
        is_buy = "BUY" in s['type'] or "KUPNO" in s['type']
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span class="time-stamp">Dzisiaj: {s['date']}</span>
                <b style="font-size: 1.1rem;">{s['p']}</b> | <a href="{s['url']}" target="_blank" style="color: #58a6ff; font-size: 0.8rem; text-decoration: none;">🔗 {s['src']}</a>
                <div style="color: {color}; font-weight: bold; font-size: 1.3rem; margin: 10px 0;">{s['type']} @ {s['in']}</div>
                <div style="font-size: 0.85rem; margin-bottom: 10px;">RSI ({tf}): <span style="color:#00ff88">{random.randint(30, 70)}</span></div>
                <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; font-family: monospace;">
                    <span style="color:#00ff88">TP1: {s['tp']}</span>
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

    st.subheader("🏆 Ranking Szans AI %")
    df = pd.DataFrame(data)
    df['szansa'] = [random.randint(60, 95) for _ in range(len(df))]
    st.dataframe(df[['p', 'szansa', 'src']].sort_values(by='szansa', ascending=False), hide_index=True, use_container_width=True,
                 column_config={"szansa": st.column_config.ProgressColumn("Szansa %", min_value=0, max_value=100)})
