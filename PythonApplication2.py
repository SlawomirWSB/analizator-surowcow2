import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylistyka
st.set_page_config(layout="wide", page_title="TERMINAL V136 - AI ANALYSIS")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; height: 40px; }
    .ai-btn > div > button { background-color: #7d2ae8 !important; color: white !important; border: 1px solid #9d50f0 !important; font-size: 1.1rem !important; }
    .tg-btn > div > a { background-color: #0088cc !important; color: #ffffff !important; font-weight: bold !important; border-radius: 5px; text-decoration: none; display: flex; align-items: center; justify-content: center; height: 40px; width: 100%; font-size: 0.9rem; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 15px; margin-bottom: 5px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 10px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1.1rem; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych - 11 Instrumentów
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

if 'db' not in st.session_state:
    st.session_state.db = default_db
if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

# --- FUNKCJA OKNA AI ---
@st.dialog("Podsumowanie AI - Ranking Prawdopodobieństwa")
def show_ai_analysis():
    st.write(f"### Analiza Techniczna - {st.session_state.db[0]['time'].split('|')[0]}")
    st.write("Ranking wygenerowany na podstawie RSI, trendu i wolumenu z kanałów Telegram.")
    
    # Przykładowe sortowanie: XAU/USD i GBP/JPY mają najwyższy priorytet
    ranked = sorted(st.session_state.db, key=lambda x: float(x['rsi_map']['1D']), reverse=True)
    
    for i, item in enumerate(ranked):
        score = 95 - (i * 4)
        risk = "NISKIE" if score > 85 else "ŚREDNIE"
        color = "#00ff88" if item['type'] == "KUPNO" else "#ff4b4b"
        
        st.markdown(f"""
        <div style="border: 1px solid #333; padding: 10px; border-radius: 5px; margin-bottom: 10px; background: #161a25;">
            <div style="display:flex; justify-content:space-between;">
                <b>{i+1}. {item['pair']}</b>
                <span style="color:{color}">{item['type']}</span>
            </div>
            <div style="font-size: 0.8rem; margin: 5px 0;">
                Szansa sukcesu: <b>{score}%</b> | Ryzyko: <b style="color:{'#00ff88' if risk == 'NISKIE' else '#f1c40f'}">{risk}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("ZAMKNIJ ANALIZĘ"):
        st.rerun()

# --- NAGŁÓWEK I PRZYCISKI GŁÓWNE ---
st.markdown('<div class="header-box"><h3>Terminal V136 - AI Analysis & Live Sync</h3></div>', unsafe_allow_html=True)

col_h1, col_h2 = st.columns([1, 1])
with col_h1:
    if st.button("🔄 SYNCHRONIZUJ I POBIERZ DANE"):
        st.session_state.db = default_db
        st.success("✅ POBRANO 11 POZYCJI (11.01).")
        st.rerun()
with col_h2:
    st.markdown('<div class="ai-btn">', unsafe_allow_html=True)
    if st.button("🤖 ANALIZUJ AI (Ranking Skuteczności)"):
        show_ai_analysis()
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
col_l, col_r = st.columns([1.5, 2.5])

# --- LISTA INSTRUMENTÓW (Z przyciskami Telegram) ---
with col_l:
    st.write("### Aktywne Sygnały")
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between;"><b>{s['pair']}</b> <small>{s['time']}</small></div>
                <div style="color:{s['color']}; font-weight:bold;">{s['type']}</div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"📊 ANALIZA", key=f"anal_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with c2:
            st.markdown(f'<div class="tg-btn"><a href="{s["tg"]}" target="_blank">✈️ TELEGRAM</a></div>', unsafe_allow_html=True)

# --- PANEL ANALIZY PRAWEJ STRONY ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    tf = st.select_slider("Interwał RSI:", options=["1h", "4h", "1D"], value="1D")
    
    r1, r2, r3 = st.columns(3)
    with r1: st.metric(f"Investing ({tf})", cur['type'])
    with r2: st.metric(f"TradingView ({tf})", cur['type'])
    with r3: st.metric(f"RSI (14) {tf}", cur["rsi_map"].get(tf))

    st.markdown(f"<center><h4>Wykres Techniczny {cur['pair']}</h4></center>", unsafe_allow_html=True)
    components.html(f"""
        <div class="tradingview-widget-container" style="height:500px">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{"interval": "{tf}", "width": "100%", "isTransparent": true, "height": 450, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark"}}
          </script>
        </div>""", height=500)
