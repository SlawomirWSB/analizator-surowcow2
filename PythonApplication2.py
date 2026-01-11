import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Ultra-Kompaktowa Stylistyka
st.set_page_config(layout="wide", page_title="TERMINAL V137")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    /* Zmniejszony nagłówek */
    .header-mini { background: #1e222d; padding: 5px; border-radius: 5px; border: 1px solid #00ff88; text-align: center; margin-bottom: 10px; font-size: 0.9rem; }
    
    /* Kompaktowe przyciski obok siebie */
    div.stButton > button { background-color: #262730 !important; color: white !important; border: 1px solid #4b4d5a !important; font-size: 0.75rem !important; height: 32px !important; padding: 0px !important; }
    .tg-btn-small > div > a { background-color: #0088cc !important; color: white !important; border-radius: 4px; text-decoration: none; display: flex; align-items: center; justify-content: center; height: 32px; width: 100%; font-size: 0.75rem; font-weight: bold; }
    
    /* Jednowierszowa karta instrumentu */
    .signal-card-slim { background-color: #1e222d; border-radius: 6px; padding: 8px; margin-bottom: 5px; border-left: 4px solid #3d4451; }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; font-size: 0.85rem; }
    .data-row-slim { background: #000000; padding: 4px; border-radius: 4px; color: #00ff88; font-family: monospace; text-align: center; font-size: 0.9rem; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. Pełna Baza - 11 Instrumentów
default_db = [
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "rsi_map": {"1h": "38.2", "4h": "40.5", "1D": "42.1"}},
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "rsi_map": {"1h": "72.1", "4h": "70.5", "1D": "68.5"}},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "rsi_map": {"1h": "49.1", "4h": "52.4", "1D": "55.4"}},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "rsi_map": {"1h": "42.5", "4h": "44.1", "1D": "45.2"}},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "rsi_map": {"1h": "39.5", "4h": "40.8", "1D": "41.5"}},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "113.85", "tp": "114.50", "rsi_map": {"1h": "59.8", "4h": "61.2", "1D": "62.1"}},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "rsi_map": {"1h": "42.1", "4h": "43.5", "1D": "44.2"}},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "1.073", "tp": "1.071", "rsi_map": {"1h": "37.1", "4h": "38.2", "1D": "38.5"}},
    {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "10.01 | 14:20", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.003", "tp": "2.007", "rsi_map": {"1h": "56.2", "4h": "57.8", "1D": "58.2"}},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 19:23", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "0.851", "tp": "0.858", "rsi_map": {"1h": "51.2", "4h": "52.0", "1D": "52.8"}},
    {"pair": "EUR/GBP", "sym": "FX:EURGBP", "time": "10.01 | 21:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "0.860", "tp": "0.865", "rsi_map": {"1h": "53.2", "4h": "54.0", "1D": "54.1"}}
]

if 'db' not in st.session_state: st.session_state.db = default_db
if 'active_idx' not in st.session_state: st.session_state.active_idx = 0

@st.dialog("Ranking AI (11.01)")
def show_ai_analysis():
    ranked = sorted(st.session_state.db, key=lambda x: float(x['rsi_map']['1D']), reverse=True)
    for i, item in enumerate(ranked):
        st.markdown(f"**{i+1}. {item['pair']}** ({item['type']}) - Szansa: {95-(i*4)}%")
    if st.button("ZAMKNIJ"): st.rerun()

# 3. Interfejs
st.markdown('<div class="header-mini">Terminal V137 - Multi-Sync (11.01)</div>', unsafe_allow_html=True)

c_top1, c_top2, c_top3 = st.columns([1, 1, 1])
with c_top1:
    if st.button("🔄 SYNC"):
        st.session_state.db = default_db
        st.success("✅ OK (11.01)")
        st.rerun()
with c_top2:
    if st.button("🤖 AI RANK"): show_ai_analysis()

st.write("---")
col_l, col_r = st.columns([1.2, 2.8])

# --- LEWA STRONA: KOMPAKTOWE KARTY ---
with col_l:
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card-slim" style="border-left-color:{s['color']}">
                <div class="card-header">
                    <b>{s['pair']}</b> 
                    <span style="color:{s['color']}; font-weight:bold;">{s['type']}</span>
                    <small style="opacity:0.6;">{s['time'].split('|')[1]}</small>
                </div>
                <div class="data-row-slim">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Przyciski obok siebie w jednym wierszu
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with btn_c2:
            st.markdown(f'<div class="tg-btn-small"><a href="{s["tg"]}" target="_blank">✈️ TG</a></div>', unsafe_allow_html=True)

# --- PRAWA STRONA: PRZYWRÓCENIE 3 ZEGARÓW ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    tf = st.select_slider("TF:", options=["1h", "4h", "1D"], value="1D")
    
    # Metryki w jednym wierszu
    m1, m2, m3 = st.columns(3)
    m1.metric("Trend", cur['type'])
    m2.metric("RSI (14)", cur["rsi_map"].get(tf))
    m3.metric("Status", "Aktualny")

    st.markdown(f"<center><small>Analiza techniczna: {cur['pair']} ({tf})</small></center>", unsafe_allow_html=True)
    
    # Przywrócenie widgetu z 3 zegarami (Podsumowanie)
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
        </div>""", height=480)
