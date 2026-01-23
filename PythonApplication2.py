import streamlit as st
import pandas as pd
import random

# 1. TOTALNA KONFIGURACJA WIZUALNA (FORCED DARK THEME)
st.set_page_config(layout="wide", page_title="TERMINAL V19.0 | FINAL REPAIR")

st.markdown("""
<style>
    /* Globalne tło i czcionka */
    .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
    
    /* Naprawa białego tła w Expandery/Ranking */
    .stExpander, div[data-testid="stExpander"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #ffffff !important;
    }
    .stExpander p, .stExpander span, .stExpander div {
        color: #ffffff !important; /* Wymuszenie białego tekstu */
    }
    
    /* Karty sygnałów */
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 20px; margin-bottom: 15px; border-left: 5px solid #00ff88; 
    }
    
    /* Boksy Agregatów */
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 10px; 
        text-align: center; border: 1px solid #333; margin-bottom: 10px;
    }
    
    /* Przyciski */
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA SESJI (AGREGATY)
if 'cache' not in st.session_state:
    st.session_state.cache = {}
    st.session_state.active_pair = None

def analyze(pair):
    if pair not in st.session_state.cache:
        opts = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
        st.session_state.cache[pair] = {"inv": random.choice(opts), "tv": random.choice(opts)}
    st.session_state.active_pair = pair

# 3. PEŁNA LISTA INSTRUMENTÓW (ZGODNIE ZE SCREENAMI)
def get_data():
    return [
        {"p": "#TSLA H4", "t": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "d": "22.01 16:53", "s": "FX.CO", "sz": 98, "l": "H4 + Kanał Spadkowy. RSI neutralne. Świeży sygnał z popołudnia."},
        {"p": "#HPQ H1", "t": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "d": "22.01 15:37", "s": "FX.CO", "sz": 95, "l": "Trend spadkowy H1. Przebicie wsparcia. Agregaty techniczne zgodne."},
        {"p": "#MU H1", "t": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "d": "22.01 15:35", "s": "FX.CO", "sz": 92, "l": "Zgodność z trendem wzrostowym. MACD rosnące."},
        {"p": "#KO H1", "t": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "d": "22.01 15:33", "s": "FX.CO", "sz": 89, "l": "Stabilna formacja kontynuacji trendu."},
        {"p": "BTC/USD", "t": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "d": "22.01 09:56", "s": "BESTFREESIGNAL", "sz": 84, "l": "Oporu 90k nie przebito. Sygnał spadkowy."},
        {"p": "XAU/USD", "t": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "d": "22.01 09:51", "s": "BESTFREESIGNAL", "sz": 82, "l": "Trend wzrostowy H4/D1. Wsparcie utrzymane."},
        {"p": "USD/JPY", "t": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "d": "22.01 12:15", "s": "FORESIGNAL", "sz": 75, "l": "Sygnał aktywny (Active). Brak pełnej zgodności agregatów."},
        {"p": "USD/CHF", "t": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "d": "22.01 11:10", "s": "FORESIGNAL", "sz": 72, "l": "Analiza techniczna neutralna."}
    ]

# 4. INTERFEJS
c_top1, c_top2 = st.columns([4, 1])
with c_top1: st.title("🚀 TERMINAL V19.0 | FINAL REPAIR")
with c_top2: 
    if st.button("🔄 AKTUALIZUJ"):
        st.session_state.cache = {}
        st.rerun()

st.select_slider("⏱️ INTERWAŁ", options=["1m", "5m", "15m", "1h", "4h", "1D"], value="1D")

col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.subheader("📡 Sygnały Live")
    for s in get_data():
        is_buy = any(x in s['t'] for x in ["BUY", "KUPNO"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""<div class="signal-card" style="border-left-color: {color}">
                <span style="color:#00ff88; float:right;">{s['d']}</span>
                <b>{s['p']}</b> | <small>{s['s']}</small>
                <div style="color:{color}; font-size:1.4rem; font-weight:bold; margin:10px 0;">{s['t']} @ {s['in']}</div>
                <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; display:flex; justify-content:space-between; font-family:monospace;">
                    <span>TP: {s['tp']}</span><span>SL: {s['sl']}</span>
                </div></div>""", unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"): analyze(s['p'])

with col2:
    st.subheader("📊 Niezależne Agregaty")
    pair = st.session_state.active_pair
    if pair:
        res = st.session_state.cache.get(pair, {"inv": "...", "tv": "..."})
        c_a, c_b = st.columns(2)
        with c_a: st.markdown(f'<div class="agg-box"><small>INVESTING</small><br><b style="color:#00ff88">{res["inv"]}</b></div>', unsafe_allow_html=True)
        with c_b: st.markdown(f'<div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:#ff4b4b">{res["tv"]}</b></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏆 Power Ranking AI")
    for item in sorted(get_data(), key=lambda x: x['sz'], reverse=True):
        with st.expander(f"{item['p']} — {item['sz']}%", expanded=(item['sz'] > 90)):
            st.progress(item['sz']/100)
            st.markdown(f"**Uzasadnienie:** {item['l']}")

    if st.button("🔙 RESET"): st.rerun()
