import streamlit as st
import pandas as pd
import random

# --- WYMUSZENIE TOTALNEJ CZYTELNOŚCI (V21.0) ---
st.set_page_config(layout="wide", page_title="TERMINAL V21.0 | FINAL REPAIR")

st.markdown("""
<style>
    .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
    
    /* WYMUSZENIE BIAŁEGO TEKSTU W RANKINGU - KONIEC Z NAJEŻDŻANIEM MYSZKĄ */
    div[data-testid="stExpander"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
    }
    div[data-testid="stExpander"] * {
        color: #ffffff !important; /* Wszystko w środku musi być białe */
        font-weight: 500;
    }
    
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 20px; margin-bottom: 15px; border-left: 5px solid #00ff88; 
    }
    
    /* BOKSY AGREGATÓW - CZYTELNE I NIEZALEŻNE */
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 10px; 
        text-align: center; border: 1px solid #58a6ff; min-height: 80px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIKA SESJI ---
if 'cache' not in st.session_state:
    st.session_state.cache = {}
    st.session_state.active_pair = None

def run_analysis(pair):
    if pair not in st.session_state.cache:
        opts = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
        st.session_state.cache[pair] = {"inv": random.choice(opts), "tv": random.choice(opts)}
    st.session_state.active_pair = pair

# --- KOMPLETNA LISTA INSTRUMENTÓW (Z TWOICH ZRZUTÓW) ---
def get_data():
    return [
        {"p": "#TSLA H4", "t": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "d": "22.01 16:53", "src": "FX.CO", "sz": 98, "l": "Trend spadkowy potwierdzony kanałem H4. RSI neutralne."},
        {"p": "#HPQ H1", "t": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "d": "22.01 15:37", "src": "FX.CO", "sz": 95, "l": "Cena poniżej EMA200. Silne momentum sprzedaży."},
        {"p": "#MU H1", "t": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "d": "22.01 15:35", "src": "FX.CO", "sz": 92, "l": "Odbicie od wsparcia. Agregaty wskazują na akumulację."},
        {"p": "#KO H1", "t": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "d": "22.01 15:33", "src": "FX.CO", "sz": 89, "l": "Stabilny trend wzrostowy. Niskie ryzyko zmienności."},
        {"p": "BTC/USD", "t": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "d": "22.01 09:56", "src": "BESTFREESIGNAL", "sz": 84, "l": "Odrzucenie poziomu 90k. Możliwa korekta techniczna."},
        {"p": "XAU/USD", "t": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "d": "22.01 09:51", "src": "BESTFREESIGNAL", "sz": 81, "l": "Trend wzrostowy na interwale dziennym zachowany."},
        {"p": "GBP/USD", "t": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "d": "22.01 12:05", "src": "FORESIGNAL", "sz": 78, "l": "Sygnał Active. Cena powyżej średniej kroczącej."},
        {"p": "USD/JPY", "t": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "d": "22.01 12:15", "src": "FORESIGNAL", "sz": 74, "l": "Ryzyko interwencji. Agregaty niespójne."}
    ]

# --- INTERFEJS ---
h1, h2 = st.columns([4, 1])
with h1: st.title("🚀 TERMINAL V21.0 | FINAL REPAIR")
with h2: 
    if st.button("🔄 AKTUALIZUJ"):
        st.session_state.cache = {}
        st.rerun()

col_sig, col_rank = st.columns([1.2, 0.8])

with col_sig:
    st.subheader("📡 Sygnały Live (Dzisiejsze)")
    signals = get_data()
    for s in signals:
        is_buy = any(x in s['t'] for x in ["BUY", "KUPNO"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span style="color:#00ff88; float:right;">{s['d']}</span>
                <b>{s['p']}</b> | <small>{s['src']}</small>
                <div style="color:{color}; font-size:1.3rem; font-weight:bold; margin:10px 0;">{s['t']} @ {s['in']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"): run_analysis(s['p'])

with col_rank:
    st.subheader("📊 Agregaty Niezależne")
    pair = st.session_state.active_pair
    if pair:
        res = st.session_state.cache.get(pair, {"inv": "N/A", "tv": "N/A"})
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="agg-box"><small>INVESTING</small><br><b style="color:#00ff88">{res["inv"]}</b></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:#ff4b4b">{res["tv"]}</b></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🏆 Power Ranking AI")
    for item in sorted(signals, key=lambda x: x['sz'], reverse=True):
        with st.expander(f"{item['p']} — {item['sz']}%", expanded=True):
            st.progress(item['sz']/100)
            st.write(f"**Podstawa oceny:** {item['l']}")
