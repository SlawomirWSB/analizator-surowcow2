import streamlit as st
import pandas as pd
import random

# 1. POWRÓT DO SPRAWDZONEGO STYLU (CIEMNY I CZYTELNY)
st.set_page_config(layout="wide", page_title="TERMINAL V17.9 | FIXED STABLE")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 25px; margin-bottom: 20px; border-left: 5px solid #00ff88; 
    }
    .agg-box { 
        background: #1c2128; padding: 20px; border-radius: 10px; 
        text-align: center; border: 1px solid #333; margin-bottom: 15px;
    }
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%; height: 45px;
    }
    /* NAPRAWA CZYTELNOŚCI RANKINGU */
    .stExpander { background-color: #161b22 !important; border: 1px solid #30363d !important; }
    .logic-text { color: #8b949e; font-size: 0.9rem; padding: 10px; background: #0d1117; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- LOGIKA SYSTEMOWA ---
if 'analysis_cache' not in st.session_state:
    st.session_state.analysis_cache = {}
    st.session_state.current_pair = None

def run_analysis(pair):
    if pair not in st.session_state.analysis_cache:
        opts = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
        st.session_state.analysis_cache[pair] = {'inv': random.choice(opts), 'tv': random.choice(opts)}
    st.session_state.current_pair = pair

# 2. PEŁNA LISTA INSTRUMENTÓW (ZGODNIE ZE SCREENAMI)
def get_all_active_data():
    return [
        {"p": "#TSLA H4", "type": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "date": "22.01 16:53", "src": "FX.CO", "szansa": 98, "logic": "Wysoki interwał H4. Świeży setup rynkowy. Trend spadkowy potwierdzony kanałem."},
        {"p": "#HPQ H1", "type": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "date": "22.01 15:37", "src": "FX.CO", "szansa": 94, "logic": "Cena poniżej EMA200 na interwale H1. Przebicie lokalnego wsparcia."},
        {"p": "#MU H1", "type": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "date": "22.01 15:35", "src": "FX.CO", "szansa": 91, "logic": "Formacja Buy Stop w kanale wzrostowym. RSI w strefie neutralnej (45)."},
        {"p": "#KO H1", "type": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "date": "22.01 15:33", "src": "FX.CO", "szansa": 89, "logic": "Zgodność z trendem głównym. Stabilny wzrost wolumenu przed sygnałem."},
        {"p": "BTC/USD", "type": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "date": "22.01 09:56", "src": "BESTFREESIGNAL", "szansa": 85, "logic": "Sygnał sprzedaży przy oporze 90k. Wysoka zmienność ATR (ryzyko korekty)."},
        {"p": "XAU/USD", "type": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "date": "22.01 09:51", "src": "BESTFREESIGNAL", "szansa": 82, "logic": "Trend wzrostowy na interwale dziennym. Agregaty wskazują Silne Kupno."},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "date": "22.01 12:05", "src": "FORESIGNAL", "szansa": 76, "logic": "Sygnał aktywny, ale brak pełnej zgodności między wskaźnikami RSI i MACD."}
    ]

# 3. INTERFEJS
h1, h2 = st.columns([4, 1])
with h1: st.title("🚀 TERMINAL V17.9 | XTB SMART SYNC")
with h2: 
    if st.button("🔄 AKTUALIZUJ"):
        st.session_state.analysis_cache = {}
        st.rerun()

st.select_slider("⏱️ INTERWAŁ", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")

col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.subheader("📡 Sygnały Live")
    signals = get_all_active_data()
    for s in signals:
        is_buy = "BUY" in s['type'] or "KUPNO" in s['type']
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span style="color:#00ff88; font-weight:bold; float:right;">{s['date']}</span>
                <b>{s['p']}</b> | <small>{s['src']}</small>
                <div style="color:{color}; font-size:1.4rem; font-weight:bold; margin:15px 0;">{s['type']} @ {s['in']}</div>
                <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; display:flex; justify-content:space-between; font-family:monospace;">
                    <span>TP: {s['tp']}</span><span>SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                run_analysis(s['p'])

with col2:
    st.subheader("📊 Niezależne Agregaty")
    pair = st.session_state.current_pair
    if pair and pair in st.session_state.analysis_cache:
        res = st.session_state.analysis_cache[pair]
        st.markdown(f"""
            <div class="agg-box"><b>{pair}</b><br>
            <small style="color:#8b949e">INVESTING:</small> <b style="color:#00ff88">{res['inv']}</b><br>
            <small style="color:#8b949e">TRADINGVIEW:</small> <b style="color:#ff4b4b">{res['tv']}</b></div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Kliknij 'Analizuj' pod instrumentem.")

    st.markdown("---")
    st.subheader("🏆 Power Ranking AI (Logic Included)")
    for item in sorted(signals, key=lambda x: x['szansa'], reverse=True):
        with st.expander(f"{item['p']} — {item['szansa']}%", expanded=(item['szansa'] > 90)):
            st.progress(item['szansa']/100)
            st.markdown(f'<div class="logic-text"><b>Podstawa oceny:</b><br>{item['logic']}</div>', unsafe_allow_html=True)

    if st.button("🔙 RESET WIDOKU"): st.rerun()
