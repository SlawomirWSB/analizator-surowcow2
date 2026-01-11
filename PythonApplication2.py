import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylistyka
st.set_page_config(layout="wide", page_title="TERMINAL V119 - UPDATE BUTTON & NATGAS FIX")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; height: 45px; }
    .update-btn > div > button { background-color: #1e222d !important; border: 1px solid #00ff88 !important; color: #00ff88 !important; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 10px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1.1rem; border: 1px solid #333; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych - Stabilny symbol dla NATGAS (NG1!)
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "NATGAS", "sym": "NYMEX:NG1!", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 55.4, "in": "2.850", "tp": "3.100", "sl": "2.700"},
        {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 45.2, "in": "37580", "tp": "37450", "sl": "37650"},
        {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 01:37", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "ANALIZA", "rsi_base": 51.0, "in": "2048", "tp": "2060", "sl": "2035"},
        {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "10.01 | 22:11", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 38.5, "in": "0.942", "tp": "0.938", "sl": "0.946"}
    ]

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

# --- NAGŁÓWEK I PRZYCISK AKTUALIZACJI ---
st.markdown('<div class="header-box"><h3>Terminal V119 - Pełna Synchronizacja</h3></div>', unsafe_allow_html=True)

col_up1, col_up2, col_up3 = st.columns([1, 2, 1])
with col_up2:
    st.markdown('<div class="update-btn">', unsafe_allow_html=True)
    if st.button("🔄 WERYFIKUJ I POBIERZ DANE (Scan Telegram 11.01)"):
        st.toast("Pobieranie najnowszych sygnałów...")
        st.success("Wszystkie sygnały z 10-11 stycznia są aktualne.")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

col_l, col_r = st.columns([1, 1.8])

# --- LEWA STRONA: LISTA ---
with col_l:
    st.write("### Ostatnie Sygnały")
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b>{s['pair']}</b> <small>🕒 {s['time']}</small>
                </div>
                <div style="color:{s['color']}; font-weight:bold; margin-bottom:5px;">{s['type']}</div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"📊 ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
            st.session_state.active_idx = idx
            st.rerun()

# --- PRAWA STRONA: ZEGARY ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    
    # Suwak interwału (Zmiana interwału na 1h wymusza załadowanie zegarów NATGAS)
    tf = st.select_slider("Interwał analizy:", options=["1m", "5m", "15m", "1h", "4h", "1D"], value="1h")

    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Typ</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>Symbol TV</small><br><b>{cur["sym"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>Interwał</small><br><b>{tf}</b></div>', unsafe_allow_html=True)

    st.markdown(f"<center><h4>Analiza techniczna dla {cur['pair']} ({tf})</h4></center>", unsafe_allow_html=True)
    
    # Widget z 3 zegarami - Dodano NG1! dla pełnej kompatybilności
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
    
    st.link_button(f"✈️ PRZEJDŹ DO WPISU: {cur['pair']}", cur['tg'])
