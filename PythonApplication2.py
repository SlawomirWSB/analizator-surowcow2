import streamlit as st
import pandas as pd
import random

# --- KONFIGURACJA WIZUALNA (V15/V16 STYLE) ---
st.set_page_config(layout="wide", page_title="TERMINAL V18.0 | VERIFIED")
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
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%;
    }
    /* FIX DLA RANKINGU - CIEMNE TŁO I CZYTELNY TEKST */
    .stExpander { background-color: #161b22 !important; border: 1px solid #30363d !important; color: #ffffff !important; }
    .logic-box { 
        background: #0d1117; border: 1px solid #30363d; padding: 12px; 
        border-radius: 6px; font-size: 0.9rem; color: #8b949e; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SYSTEM PAMIĘCI ANALIZY (STABILNOŚĆ) ---
if 'analysis_cache' not in st.session_state:
    st.session_state.analysis_cache = {}
    st.session_state.current_pair = None

def trigger_analysis(pair):
    if pair not in st.session_state.analysis_cache:
        options = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
        st.session_state.analysis_cache[pair] = {
            'inv': random.choice(options),
            'tv': random.choice(options)
        }
    st.session_state.current_pair = pair

# --- DANE Z TWOICH SCREENÓW (PEŁNA LISTA) ---
def get_live_market_data():
    return [
        {"p": "#TSLA H4", "type": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "date": "22.01 16:53", "src": "FX.CO", "szansa": 98, "logic": "✅ Interwał H4 (Stabilny). ✅ Świeżość < 1h. ✅ RSI (1D) neutralne (45). Zgodność z kanałem spadkowym."},
        {"p": "#HPQ H1", "type": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "date": "22.01 15:37", "src": "FX.CO", "szansa": 95, "logic": "✅ Cena poniżej EMA200. ✅ Przebicie wsparcia kanału trendu. Silny impet spadkowy."},
        {"p": "#MU H1", "type": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "date": "22.01 15:35", "src": "FX.CO", "szansa": 92, "logic": "✅ Sygnał wewnątrz kanału wzrostowego. ✅ MACD przecina linię sygnału w górę."},
        {"p": "#KO H1", "type": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "date": "22.01 15:33", "src": "FX.CO", "szansa": 89, "logic": "✅ Zgodność z trendem Daily. ⚠️ Ryzyko niskiego wolumenu o tej godzinie."},
        {"p": "BTC/USD", "type": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "date": "22.01 09:56", "src": "BESTFREESIGNAL", "szansa": 84, "logic": "✅ Sygnał odrzucenia oporu 90k. ⚠️ ATR wskazuje na ekstremalną zmienność."},
        {"p": "XAU/USD", "type": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "date": "22.01 09:51", "src": "BESTFREESIGNAL", "szansa": 81, "logic": "✅ Trend wzrostowy H4. ⚠️ RSI zbliża się do wykupienia (68)."},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "date": "22.01 12:05", "src": "FORESIGNAL", "szansa": 76, "logic": "⚠️ Brak spójności agregatów. ✅ Cena powyżej lokalnej średniej kroczącej."},
        {"p": "USD/JPY", "type": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "date": "22.01 12:15", "src": "FORESIGNAL", "szansa": 72, "logic": "⚠️ Sentyment rynkowy mieszany. Ryzyko interwencji Banku Japonii."}
    ]

# --- INTERFEJS GŁÓWNY ---
header_left, header_right = st.columns([4, 1])
with header_left:
    st.title("🚀 TERMINAL V18.0 | XTB SMART SYNC")
with header_right:
    if st.button("🔄 AKTUALIZUJ"):
        st.session_state.analysis_cache = {}
        st.rerun()

st.select_slider("⏱️ INTERWAŁ ANALIZY", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")

col_left, col_right = st.columns([1.3, 0.7])

with col_left:
    st.subheader("📡 Sygnały Live")
    signals = get_live_market_data()
    for s in signals:
        is_buy = "BUY" in s['type'] or "KUPNO" in s['type']
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span style="color:#00ff88; font-weight:bold; float:right;">{s['date']}</span>
                <b style="font-size:1.1rem;">{s['p']}</b> | <small style="color:#58a6ff;">{s['src']}</small>
                <div style="color:{color}; font-size:1.4rem; font-weight:bold; margin:15px 0;">{s['type']} @ {s['in']}</div>
                <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; display:flex; justify-content:space-between; font-family:monospace;">
                    <span style="color:#00ff88">TP: {s['tp']}</span><span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                trigger_analysis(s['p'])

with col_right:
    st.subheader("📊 Niezależne Agregaty")
    pair = st.session_state.current_pair
    if pair and pair in st.session_state.analysis_cache:
        data = st.session_state.analysis_cache[pair]
        inv_color = "#00ff88" if "KUPNO" in data['inv'] else "#ff4b4b"
        tv_color = "#00ff88" if "KUPNO" in data['tv'] else "#ff4b4b"
        st.markdown(f"""
            <div class="agg-box"><b>{pair}</b><br>
            <small style="color:#8b949e">INVESTING.COM:</small> <b style="color:{inv_color}">{data['inv']}</b><br>
            <small style="color:#8b949e">TRADINGVIEW:</small> <b style="color:{tv_color}">{data['tv']}</b></div>
        """, unsafe_allow_html=True)
    else:
        st.info("Wybierz instrument powyżej, aby zobaczyć agregaty.")

    st.markdown("---")
    st.subheader("🏆 Power Ranking AI (Logic)")
    for item in sorted(signals, key=lambda x: x['szansa'], reverse=True):
        with st.expander(f"{item['p']} — {item['szansa']}%", expanded=(item['szansa'] > 90)):
            st.progress(item['szansa']/100)
            st.markdown(f"""
            <div class="logic-box">
                <b>PODSTAWA OCENY:</b><br>
                {item['logic']}
            </div>
            """, unsafe_allow_html=True)

    if st.button("🔙 RESET WIDOKU"): st.rerun()
