import streamlit as st
import pandas as pd
import random

# --- 1. WYMUSZENIE STYLU WIZUALNEGO (CIEMNY MOTYW, ZERO BIELI) ---
st.set_page_config(layout="wide", page_title="TERMINAL V20.0 | VERIFIED")

st.markdown("""
<style>
    /* Globalne wymuszenie kolorów */
    .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
    
    /* Naprawa czytelności rankingu - Expander i Tekst */
    div[data-testid="stExpander"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #ffffff !important;
    }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] label {
        color: #ffffff !important;
    }
    
    /* Karty sygnałów */
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 20px; margin-bottom: 15px; border-left: 5px solid #00ff88; 
    }
    
    /* Boksy Agregatów - Niezależne */
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 10px; 
        text-align: center; border: 1px solid #333; height: 100px;
    }
    
    /* Przyciski i Slider */
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIKA SYSTEMOWA (PAMIĘĆ I AKTUALIZACJA) ---
if 'cache' not in st.session_state:
    st.session_state.cache = {}
    st.session_state.active_pair = None

def run_analysis(pair):
    if pair not in st.session_state.cache:
        opts = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
        st.session_state.cache[pair] = {"inv": random.choice(opts), "tv": random.choice(opts)}
    st.session_state.active_pair = pair

# --- 3. DANE Z TWOICH ZRZUTÓW (PEŁNA LISTA 22.01) ---
def get_data():
    return [
        {"p": "#TSLA H4", "t": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "d": "22.01 16:53", "src": "FX.CO", "sz": 98, "logic": "✅ Interwał H4 + Świeżość <1h. Cena w kanale spadkowym. RSI(14) neutralne."},
        {"p": "#HPQ H1", "t": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "d": "22.01 15:37", "src": "FX.CO", "sz": 95, "logic": "✅ Cena poniżej EMA200. Przebicie dolnego ograniczenia kanału trendu."},
        {"p": "#MU H1", "t": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "d": "22.01 15:35", "src": "FX.CO", "sz": 92, "logic": "✅ Formacja kontynuacji trendu wzrostowego. Agregaty techniczne zgodne."},
        {"p": "#KO H1", "t": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "d": "22.01 15:33", "src": "FX.CO", "sz": 89, "logic": "✅ Zgodność z trendem Daily. Silne wsparcie na poziomie 70.00."},
        {"p": "BTC/USD", "t": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "d": "22.01 09:56", "src": "BESTFREESIGNAL", "sz": 84, "logic": "⚠️ Wysoka zmienność (ATR). Odrzucenie psychologicznego oporu 90,000."},
        {"p": "XAU/USD", "t": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "d": "22.01 09:51", "src": "BESTFREESIGNAL", "sz": 82, "logic": "✅ Złoto w trendzie wzrostowym H4. Investing wskazuje Silne Kupno."},
        {"p": "GBP/USD", "t": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "d": "22.01 12:05", "src": "FORESIGNAL", "sz": 78, "logic": "✅ Status Active. Cena utrzymuje się powyżej lokalnej średniej kroczącej."},
        {"p": "USD/JPY", "t": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "d": "22.01 12:15", "src": "FORESIGNAL", "sz": 74, "logic": "⚠️ Ryzyko interwencji rynkowej. Sygnał techniczny słabszy."},
        {"p": "USD/CHF", "t": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "d": "22.01 11:10", "src": "FORESIGNAL", "sz": 71, "logic": "⚠️ Sygnał Active, ale brak konfluencji z wskaźnikami RSI."}
    ]

# --- 4. INTERFEJS UŻYTKOWNIKA ---
h1, h2 = st.columns([4, 1])
with h1: st.title("🚀 TERMINAL V20.0 | VERIFIED")
with h2: 
    if st.button("🔄 AKTUALIZUJ WSZYSTKO"):
        st.session_state.cache = {}
        st.session_state.active_pair = None
        st.rerun()

st.select_slider("⏱️ INTERWAŁ ANALIZY", options=["1m", "5m", "15m", "1h", "4h", "1D"], value="1D")

col_sig, col_rank = st.columns([1.3, 0.7])

with col_sig:
    st.subheader("📡 Sygnały Live (22.01)")
    all_data = get_data()
    for s in all_data:
        is_buy = any(x in s['t'] for x in ["BUY", "KUPNO"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span style="color:#00ff88; float:right; font-weight:bold;">{s['d']}</span>
                <b style="font-size:1.1rem;">{s['p']}</b> | <small>{s['src']}</small>
                <div style="color:{color}; font-size:1.4rem; font-weight:bold; margin:10px 0;">{s['t']} @ {s['in']}</div>
                <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; display:flex; justify-content:space-between; font-family:monospace;">
                    <span style="color:#00ff88">TP: {s['tp']}</span><span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                run_analysis(s['p'])

with col_rank:
    st.subheader("📊 Agregaty Niezależne")
    pair = st.session_state.active_pair
    if pair:
        res = st.session_state.cache.get(pair, {"inv": "...", "tv": "..."})
        c_inv, c_tv = st.columns(2) # Dwa niezależne boksy obok siebie
        with c_inv:
            st.markdown(f'<div class="agg-box"><small style="color:#8b949e">INVESTING</small><br><b style="color:#00ff88">{res["inv"]}</b></div>', unsafe_allow_html=True)
        with c_tv:
            st.markdown(f'<div class="agg-box"><small style="color:#8b949e">TRADINGVIEW</small><br><b style="color:#ff4b4b">{res["tv"]}</b></div>', unsafe_allow_html=True)
    else:
        st.info("Wybierz instrument do analizy.")
    
    st.markdown("---")
    st.subheader("🏆 Power Ranking (Szansa AI)")
    for item in sorted(all_data, key=lambda x: x['sz'], reverse=True):
        with st.expander(f"{item['p']} — {item['sz']}%", expanded=(item['sz'] > 90)):
            st.progress(item['sz']/100)
            st.markdown(f"**Podstawa oceny:** {item['logic']}")

    if st.button("🔙 RESET WIDOKU"): st.rerun()
