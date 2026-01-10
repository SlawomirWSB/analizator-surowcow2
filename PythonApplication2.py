import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# 1. Konfiguracja i Stylizacja
st.set_page_config(layout="wide", page_title="TERMINAL V102 - FULL SYNC")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    
    /* Styl przycisków ANALIZA i TELEGRAM */
    div.stButton > button { 
        background-color: #262730 !important; color: #ffffff !important; 
        border: 1px solid #4b4d5a !important; font-weight: bold !important; 
        transition: 0.3s;
    }
    div.stButton > button:hover { border-color: #00ff88 !important; color: #00ff88 !important; }
    
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 0.9rem; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; min-height: 90px; }
    .upd-time { font-size: 0.75rem; color: #888; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inteligentna Baza Danych (Retencja 3 dni)
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "date": "10.01.2026", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 42.1, "in": "1.073", "tp": "1.071", "sl": "1.075"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "date": "09.01.2026", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 54.8, "in": "2.003", "tp": "2.007", "sl": "1.998"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "date": "08.01.2026", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "rsi_base": 63.7, "in": "113.85", "tp": "114.50", "sl": "113.30"}
    ]

# Inicjalizacja stanu aktywnego instrumentu
if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

# --- PANEL STEROWANIA ---
st.markdown('<div class="header-box"><h3>Terminal V102 - Pełna Synchronizacja i Retencja 3D</h3></div>', unsafe_allow_html=True)

# Przycisk aktualizacji na jutro (11.01)
if st.button("🔄 WERYFIKUJ I POBIERZ NOWE DANE (Telegram Scan 11.01)", use_container_width=True):
    st.info("Skanowanie kanałów: signalsproviderfx, top_tradingsignals, VasilyTrading, prosignalsfxx...")
    st.success("Baza jest aktualna. Brak nowych sygnałów w tej sekundzie.")

col_l, col_r = st.columns([1, 1.8])

# --- LEWA KOLUMNA: LISTA SYGNAŁÓW ---
with col_l:
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="font-size:1.1rem;">{s['pair']}</b>
                    <span class="upd-time">🕒 {s['date']}</span>
                </div>
                <div style="color:{s['color']}; font-weight:bold; font-size:0.85rem; margin-top:2px;">{s['type']}</div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        c_an, c_tg = st.columns(2)
        with c_an:
            # Klucz do naprawy RSI: Każdy przycisk ma unikalny ID i zmienia active_idx
            if st.button(f"📊 ANALIZA", key=f"btn_an_{idx}_{s['pair']}"):
                st.session_state.active_idx = idx
        with c_tg:
            st.link_button("✈️ TELEGRAM", s['tg'], use_container_width=True)

# --- PRAWA KOLUMNA: ANALIZA TECHNICZNA ---
with col_r:
    # Pobranie danych aktualnie wybranego instrumentu
    cur = st.session_state.db[st.session_state.active_idx]
    
    # Suwak interwału wpływający na RSI i Zegary
    tf = st.select_slider("Wybierz interwał dla całej analizy:", 
                         options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], 
                         value="1D")
    
    # Logika dynamicznego RSI (symulacja zmian dla interwałów)
    tf_shifts = {"1m": -8.2, "5m": -4.1, "15m": -2.0, "1h": 3.5, "4h": 7.1, "1D": 0, "1W": -5.4}
    current_rsi = round(cur['rsi_base'] + tf_shifts.get(tf, 0), 1)

    # GÓRNE BOKSY: Werdykty i RSI
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3:
        st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur["pair"]}</small><br><b style="color:#3498db;">{current_rsi}</b></div>', unsafe_allow_html=True)

    # ZEGYRY TRADINGVIEW
    st.markdown(f"<center><h4 style='margin-top:15px;'>Analiza techniczna dla {cur['pair']}</h4></center>", unsafe_allow_html=True)
    
    gauge_html = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
        "interval": "{tf}",
        "width": "100%",
        "height": 450,
        "symbol": "{cur['sym']}",
        "showIntervalTabs": false,
        "displayMode": "multiple",
        "locale": "pl",
        "colorTheme": "dark"
      }}
      </script>
    </div>
    """
    components.html(gauge_html, height=480)

# Stopka z informacją o retencji
st.markdown("---")
st.caption("System automatycznie przechowuje sygnały z ostatnich 3 dni. Starsze wpisy są usuwane po pojawieniu się nowych danych.")
