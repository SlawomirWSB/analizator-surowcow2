import streamlit as st
import pandas as pd
import random

# 1. KONFIGURACJA I STYL
st.set_page_config(layout="wide", page_title="TERMINAL V17.7 | EXPLAINABLE AI")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 25px; margin-bottom: 20px; border-left: 5px solid #00ff88; 
    }
    .logic-box {
        background: rgba(88, 166, 255, 0.05);
        border: 1px dashed #30363d;
        border-radius: 5px;
        padding: 10px;
        margin-top: 5px;
        font-size: 0.85rem;
        color: #8b949e;
    }
    .agg-box { 
        background: #1c2128; padding: 20px; border-radius: 10px; 
        text-align: center; border: 1px solid #333; margin-bottom: 15px;
    }
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%; height: 45px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIKA SYSTEMOWA ---
if 'analysis_cache' not in st.session_state:
    st.session_state.analysis_cache = {}
    st.session_state.current_pair = None

def get_stable_analysis(pair_name):
    if pair_name not in st.session_state.analysis_cache:
        options = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
        st.session_state.analysis_cache[pair_name] = {
            'inv': random.choice(options),
            'tv': random.choice(options)
        }
    st.session_state.current_pair = pair_name

# 2. DANE I GENERATOR WYJAŚNIEŃ (LOGIKA RANKINGU)
def get_ranked_data():
    signals = [
        {"p": "#TSLA H4", "szansa": 98, "src": "FX.CO", "date": "16:53", "logic": "✅ Najwyższy interwał (H4). ✅ Zgodność z kanałem spadkowym. ✅ Świeżość < 1h. ✅ RSI w strefie neutralnej."},
        {"p": "#HPQ H1", "szansa": 92, "src": "FX.CO", "date": "15:37", "logic": "✅ Formacja Sell Stop potwierdzona. ✅ Cena poniżej EMA200. ⚠️ Niższy interwał niż TSLA."},
        {"p": "BTC/USD", "szansa": 89, "src": "BESTFREESIGNAL", "date": "09:56", "logic": "✅ Precyzyjne TP/SL. ⚠️ Wysoka zmienność (ATR). ⚠️ Sygnał poranny - ryzyko konsolidacji."},
        {"p": "XAU/USD", "szansa": 85, "src": "BESTFREESIGNAL", "date": "09:51", "logic": "✅ Trend wzrostowy. ⚠️ RSI zbliża się do poziomu wykupienia (68)."},
        {"p": "GBP/USD", "szansa": 78, "src": "FORESIGNAL", "date": "12:05", "logic": "✅ Status Active. ❌ Brak spójności między Investing (Kupno) a TV (Sprzedaż)."},
        {"p": "USD/JPY", "szansa": 72, "src": "FORESIGNAL", "date": "12:15", "logic": "⚠️ Sentyment rynkowy neutralny. ⚠️ Ryzyko interwencji na JPY."}
    ]
    return signals

# 3. INTERFEJS
h_col1, h_col2 = st.columns([4, 1])
with h_col1: st.title("🚀 TERMINAL V17.7 | EXPLAINABLE AI")
with h_col2: 
    if st.button("🔄 AKTUALIZUJ"):
        st.session_state.analysis_cache = {}
        st.rerun()

c1, c2 = st.columns([1.2, 0.8])

with c1:
    st.subheader("📡 Sygnały Live")
    for s in [x for x in get_ranked_data()]:
        is_buy = any(x in s['p'] for x in ["XAU", "GBP", "MU"]) # uproszczone dla demo
        color = "#00ff88" if s['szansa'] > 80 else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span style="color:#8b949e; float:right;">{s['date']}</span>
                <b>{s['p']}</b> | <small>{s['src']}</small>
                <div style="color:{color}; font-size:1.3rem; font-weight:bold; margin:10px 0;">{s['szansa']}% Szansy</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                get_stable_analysis(s['p'])

with c2:
    st.subheader("📊 Analiza i Uzasadnienie")
    
    # AGREGATY
    pair = st.session_state.current_pair
    if pair:
        res = st.session_state.analysis_cache.get(pair, {"inv": "...", "tv": "..."})
        st.markdown(f"""
            <div class="agg-box"><b>{pair}</b><br><small>INVESTING:</small> <span style="color:#00ff88">{res['inv']}</span><br>
            <small>TRADINGVIEW:</small> <span style="color:#ff4b4b">{res['tv']}</span></div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏆 Power Ranking AI")
    
    # ROZSZERZONY RANKING Z WYJAŚNIENIAMI
    ranked_list = get_ranked_data()
    for item in sorted(ranked_list, key=lambda x: x['szansa'], reverse=True):
        with st.expander(f"{item['p']} - {item['szansa']}%", expanded=True):
            st.progress(item['szansa']/100)
            st.markdown(f"""
            <div class="logic-box">
                <b>Podstawa oceny:</b><br>
                {item['logic']}
            </div>
            """, unsafe_allow_html=True)

    if st.button("🔙 RESET"): st.rerun()
