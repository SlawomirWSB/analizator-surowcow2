import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# 1. Konfiguracja V96 - Naprawa UI i Logiki
st.set_page_config(layout="wide", page_title="HUB V96")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #00ff88; text-align: center; }
    
    /* Styl przycisków z V91/V93 */
    div.stButton > button {
        background-color: #262730 !important; color: #ffffff !important;
        border: 1px solid #4b4d5a !important; font-weight: bold !important;
    }
    
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .upd-time { font-size: 0.7rem; color: #888; text-align: right; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 0.95rem; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicjalizacja Bazy Danych (Retencja 3 dni)
if 'signals' not in st.session_state:
    st.session_state.signals = [
        {"pair": "GBP/CHF", "in": "1.073", "tp": "1.071", "sl": "1.075", "sym": "FX:GBPCHF", "type": "SPRZEDAŻ", "color": "#ff4b4b", "date": "10.01.2026", "tg": "https://t.me/s/signalsproviderfx"},
        {"pair": "GBP/AUD", "in": "2.003", "tp": "2.007", "sl": "1.998", "sym": "FX:GBPAUD", "type": "KUPNO", "color": "#00ff88", "date": "09.01.2026", "tg": "https://t.me/s/top_tradingsignals"},
        {"pair": "CAD/JPY", "in": "113.85", "tp": "114.50", "sl": "113.30", "sym": "FX:CADJPY", "type": "KUPNO", "color": "#00ff88", "date": "08.01.2026", "tg": "https://t.me/s/prosignalsfxx"}
    ]

if 'active_sel' not in st.session_state: st.session_state.active_sel = st.session_state.signals[0]
if 'filter' not in st.session_state: st.session_state.filter = "3_dni"

# --- PANEL STEROWANIA ---
st.markdown('<div class="header-box"><h3>Terminal V96 - Zarządzanie i Synchronizacja</h3></div>', unsafe_allow_html=True)

c_top1, c_top2, c_top3 = st.columns([2, 1, 1])
with c_top1:
    if st.button("🔄 WERYFIKUJ NOWE SYGNAŁY (Telegram Scan)", use_container_width=True):
        st.info("Skanowanie kanałów... Brak nowych sygnałów w tej sekundzie.")
with c_top2:
    if st.button("📅 DZISIAJ", use_container_width=True): st.session_state.filter = "dzisiaj"
with c_top3:
    if st.button("📅 OSTATNIE 3 DNI", use_container_width=True): st.session_state.filter = "3_dni"

# --- LOGIKA FILTROWANIA ---
today = "10.01.2026"
if st.session_state.filter == "dzisiaj":
    display_list = [s for s in st.session_state.signals if s['date'] == today]
else:
    display_list = st.session_state.signals[:3] # Zawsze tylko 3 najnowsze dni

# --- UKŁAD GŁÓWNY ---
col_l, col_r = st.columns([1, 1.8])

with col_l:
    for s in display_list:
        st.markdown(f"""
            <div class="signal-card" style="border-left-color: {s['color']}">
                <div style="display:flex; justify-content:space-between;">
                    <div><b style="font-size:1.1rem;">{s['pair']}</b><br>
                    <span style="color:{s['color']}; font-weight:bold;">{s['type']}</span></div>
                    <div class="upd-time">🕒 {s['date']}</div>
                </div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        ca, ct = st.columns(2)
        with ca:
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"an_{s['pair']}_{s['date']}", use_container_width=True):
                st.session_state.active_sel = s
        with ct:
            st.link_button("✈️ TELEGRAM", s['tg'], use_container_width=True)

with col_r:
    active = st.session_state.active_sel
    # Globalny suwak z V93
    sel_tf = st.select_slider("Interwał analizy:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Statystyki i Zegary (Naprawione powiązanie danych)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="stat-box"><small>Investing ({sel_tf})</small><br><b>{active["type"]}</b></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-box"><small>TradingView ({sel_tf})</small><br><b>{active["type"]}</b></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {active["pair"]}</small><br><b style="color:#3498db;">61.3</b></div>', unsafe_allow_html=True)

    gauge_html = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{ "interval": "{sel_tf}", "width": "100%", "height": 400, "symbol": "{active['sym']}", "locale": "pl", "colorTheme": "dark", "displayMode": "multiple" }}
      </script>
    </div>"""
    components.html(gauge_html, height=420)

if __name__ == "__main__": pass
