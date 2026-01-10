import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# 1. Konfiguracja V95
st.set_page_config(layout="wide", page_title="HUB V95 - Smart History")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #00ff88; text-align: center; }
    
    /* Naprawa widoczności przycisków z V91 */
    div.stButton > button {
        background-color: #262730 !important; color: #ffffff !important;
        border: 1px solid #4b4d5a !important; font-weight: bold !important;
    }
    
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; }
    .upd-time { font-size: 0.7rem; color: #888; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# Symulacja bazy danych z datami
if 'signals_db' not in st.session_state:
    st.session_state.signals_db = [
        {"pair": "GBP/CHF", "in": "1.073", "tp": "1.071", "sl": "1.075", "type": "SPRZEDAŻ", "color": "#ff4b4b", "date": datetime.now().strftime("%d.%m.%Y"), "sym": "FX:GBPCHF", "tg": "https://t.me/s/signalsproviderfx"},
        {"pair": "GBP/AUD", "in": "2.003", "tp": "2.007", "sl": "1.998", "type": "KUPNO", "color": "#00ff88", "date": (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y"), "sym": "FX:GBPAUD", "tg": "https://t.me/s/top_tradingsignals"},
        {"pair": "CAD/JPY", "in": "113.85", "tp": "114.50", "sl": "113.30", "type": "KUPNO", "color": "#00ff88", "date": (datetime.now() - timedelta(days=2)).strftime("%d.%m.%Y"), "sym": "FX:CADJPY", "tg": "https://t.me/s/prosignalsfxx"}
    ]
if 'view_mode' not in st.session_state: st.session_state.view_mode = "3_dni"

# --- PANEL STEROWANIA ---
st.markdown('<div class="header-box"><h3>Terminal V95 - Zarządzanie Sygnałami</h3></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.5, 1, 1])
with c1:
    if st.button("🔄 WERYFIKUJ I AKTUALIZUJ DANE", use_container_width=True):
        st.info("Sprawdzanie kanałów: signalsproviderfx, top_tradingsignals, VasilyTrading, prosignalsfxx...")
        # Tutaj logika scrapera - jeśli brak zmian, nic nie robi
with c2:
    if st.button("📅 TYLKO DZISIAJ", use_container_width=True): st.session_state.view_mode = "dzisiaj"
with c3:
    if st.button("📅 OSTATNIE 3 DNI", use_container_width=True): st.session_state.view_mode = "3_dni"

# --- FILTROWANIE DANYCH ---
today_str = datetime.now().strftime("%d.%m.%Y")
if st.session_state.view_mode == "dzisiaj":
    display_data = [s for s in st.session_state.signals_db if s['date'] == today_str]
else:
    # Retencja 3 dni
    display_data = st.session_state.signals_db[:3] 

# --- WIDOK GŁÓWNY ---
col_l, col_r = st.columns([1, 1.8])

with col_l:
    if not display_data:
        st.warning("Brak nowych sygnałów dla wybranego filtru.")
    for d in display_data:
        st.markdown(f"""
            <div class="signal-card" style="border-left-color: {d['color']}">
                <div style="display:flex; justify-content:space-between;">
                    <div><b>{d['pair']}</b><br><small style="color:{d['color']}">{d['type']}</small></div>
                    <div class="upd-time">🕒 {d['date']}</div>
                </div>
                <div class="data-row">IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}</div>
            </div>
        """, unsafe_allow_html=True)
        # Przyciski ANALIZA z V91
        if st.button(f"📊 ANALIZA {d['pair']}", key=f"an_{d['pair']}", use_container_width=True):
            st.session_state.active_pair = d
        st.link_button("✈️ TELEGRAM", d['tg'], use_container_width=True)

with col_r:
    active = st.session_state.get('active_pair', st.session_state.signals_db[0])
    sel_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Zegary i RSI z V85/V93
    st.markdown(f"#### Analiza Techniczna: {active['pair']} ({sel_tf})")
    gauge_html = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{ "interval": "{sel_tf}", "width": "100%", "height": 400, "symbol": "{active['sym']}", "locale": "pl", "colorTheme": "dark", "displayMode": "multiple" }}
      </script>
    </div>"""
    components.html(gauge_html, height=420)

if __name__ == "__main__": pass
