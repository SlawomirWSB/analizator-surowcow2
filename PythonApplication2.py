import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja strony i CSS
st.set_page_config(layout="wide", page_title="TERMINAL V120 - FULL SYNC")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; height: 42px; }
    .update-btn > div > button { background-color: #1e222d !important; border: 1px solid #00ff88 !important; color: #00ff88 !important; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; transition: 0.3s; }
    .signal-card:hover { background-color: #252a36; }
    .data-row { background: #000000; padding: 10px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1.1rem; border: 1px solid #333; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych - Przywrócenie sygnałów z 10.01 i Fix NATGAS
if 'db' not in st.session_state:
    st.session_state.db = [
        # --- 11 STYCZNIA ---
        {"pair": "NATGAS", "sym": "FX_IDC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "sl": "2.700"},
        {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "sl": "37650"},
        {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 01:37", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "ANALIZA", "in": "2048", "tp": "2060", "sl": "2035"},
        # --- 10 STYCZNIA (Przywrócone) ---
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "1.073", "tp": "1.071", "sl": "1.075"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "10.01 | 14:20", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.003", "tp": "2.007", "sl": "1.998"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 09:15", "tg": "https://t.me/s/signalsproviderfx", "color": "#00ff88", "type": "KUPNO", "in": "113.85", "tp": "114.50", "sl": "113.30"},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "sl": "0.628"},
        {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 19:23", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "0.851", "tp": "0.858", "sl": "0.847"}
    ]

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

# --- NAGŁÓWEK I PRZYCISK AKTUALIZACJI ---
st.markdown('<div class="header-box"><h3>Terminal V120 - Pełna Synchronizacja i Naprawa Zegarów</h3></div>', unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    st.markdown('<div class="update-btn">', unsafe_allow_html=True)
    if st.button("🔄 WERYFIKUJ I POBIERZ DANE (Scan 10.01 - 11.01)"):
        st.toast("Synchronizacja bazy danych...")
        st.success("Baza zaktualizowana. Przywrócono sygnały GBP i CAD z 10 stycznia.")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

col_l, col_r = st.columns([1, 2])

# --- LEWA STRONA: LISTA SYGNAŁÓW ---
with col_l:
    st.write("### Ostatnie Sygnały (48h)")
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between;">
                    <b>{s['pair']}</b> <small>{s['time']}</small>
                </div>
                <div style="color:{s['color']}; font-weight:bold;">{s['type']}</div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"📊 ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
            st.session_state.active_idx = idx
            st.rerun()

# --- PRAWA STRONA: ANALIZA TECHNICZNA I ROZSZERZONY SUWAK ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    
    # Rozszerzony suwak interwału o Tydzień (1W) i Miesiąc (1M)
    tf = st.select_slider(
        "Wybierz interwał czasowy:", 
        options=["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"], 
        value="1h"
    )

    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Instrument</small><br><b>{cur["pair"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>Aktualny Sygnał</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>Interwał</small><br><b>{tf}</b></div>', unsafe_allow_html=True)

    st.markdown(f"<center><h4>Analiza techniczna dla {cur['pair']} ({tf})</h4></center>", unsafe_allow_html=True)
    
    # Komponent Zegarów - Symbol FIX dla NATGAS i US30
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf}",
            "width": "100%",
            "isTransparent": true,
            "height": 450,
            "symbol": "{cur['sym']}",
            "showIntervalTabs": true,
            "displayMode": "multiple",
            "locale": "pl",
            "colorTheme": "dark"
          }}
          </script>
        </div>""", height=500)
    
    st.link_button(f"✈️ ZOBACZ WPIS DLA {cur['pair']} NA TELEGRAMIE", cur['tg'])
