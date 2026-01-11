import streamlit as st
import streamlit.components.v1 as components

# 1. Zaawansowana Konfiguracja Stylu (Mobilna Optymalizacja)
st.set_page_config(layout="wide", page_title="TERMINAL V145", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa widoczności tekstu przycisków */
    div.stButton > button { 
        background-color: #262730 !important; 
        color: #ffffff !important; 
        border: 1px solid #00ff88 !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 4px 1px !important;
        font-size: 0.7rem !important;
    }

    .signal-card-v145 { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 6px; border-left: 5px solid #3d4451; }
    .card-top { display: flex; justify-content: space-between; align-items: center; }
    .pair-title { font-size: 0.9rem; font-weight: bold; }
    .time-stamp { font-size: 0.7rem; color: #00ff88; }
    .data-row { background: #000; padding: 6px; border-radius: 5px; color: #00ff88; font-family: monospace; text-align: center; margin: 5px 0; border: 1px solid #333; font-size: 0.8rem; }

    /* Kompaktowy przycisk TG */
    .tg-small { 
        background-color: #0088cc; color: white !important; text-decoration: none; 
        display: flex; align-items: center; justify-content: center; 
        height: 30px; border-radius: 4px; font-weight: bold; font-size: 0.7rem; 
        border: 1px solid #4b4d5a; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych z RSI i Polską Analizą
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "conf": 94, "rsi": 68.5, "basis": "Silny impet, odbicie od wsparcia, RSI w strefie wzrostowej."},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "conf": 89, "rsi": 72.1, "basis": "RSI wykupione, przecięcie EMA, opór na 211.70."},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "conf": 87, "rsi": 42.5, "basis": "Niedźwiedzia dywergencja, odrzucenie poziomu oporu."},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "conf": 82, "rsi": 31.2, "basis": "RSI blisko wyprzedania, linia trendu wzrostowego na H4."},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "conf": 78, "rsi": 41.5, "basis": "Formacja niższych szczytów, opór na zniesieniu Fibo."},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "113.85", "tp": "114.50", "conf": 75, "rsi": 55.4, "basis": "Wsparcie MA 200, stabilny wzrost wolumenu kupna."},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "conf": 72, "rsi": 48.9, "basis": "Test oporu 0.624, sygnał Price Action z Fibo 0.618."}
]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0

# 3. PRZYWRÓCONE OKNO RANKINGU Z WARTOŚCIĄ RSI
@st.dialog("🤖 RANKING AI + RSI (11.01)")
def show_ai_ranking_rsi():
    st.write("Ranking wielowskaźnikowy (Sygnały posegregowane):")
    ranked = sorted(db, key=lambda x: x['conf'], reverse=True)
    for i, item in enumerate(ranked):
        clr = "#00ff88" if item['conf'] > 80 else "#ff9800"
        st.markdown(f"""
            **{i+1}. {item['pair']}** | Szansa: <span style="color:{clr};">{item['conf']}%</span> | **RSI: {item['rsi']}** *Analiza:* {item['basis']}  
            ---
        """, unsafe_allow_html=True)
    if st.button("ZAMKNIJ"): st.rerun()

# --- NAGŁÓWEK ---
st.markdown('<div style="background:#1e222d; padding:8px; border-radius:5px; border:1px solid #00ff88; text-align:center; margin-bottom:10px; font-size:0.75rem;">TERMINAL V145 | AI Analysis + RSI Recovery</div>', unsafe_allow_html=True)

# WIERSZ PRZYCISKÓW GÓRNYCH
c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🔄 SYNC"): st.rerun()
with c_nav2:
    if st.button("🤖 AI RANK"): show_ai_ranking_rsi()

st.write("---")
col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA STRONA: SYGNAŁY (Układ 1+1) ---
with col_l:
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card-v145" style="border-left-color:{s['color']}">
                <div class="card-top">
                    <span class="pair-title">{s['pair']} <span style="color:{s['color']}">{s['type']}</span></span>
                    <span class="time-stamp">{s['time']}</span>
                </div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with b2:
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-small">✈️ TG</a>', unsafe_allow_html=True)

# --- PRAWA STRONA: AGREGATY ---
with col_r:
    cur = db[st.session_state.active_idx]
    tf = st.select_slider("TF:", options=["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"], value="1D")
    
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Invest", cur['type'])
    m2.metric("TV", cur['type'])
    m3.metric(f"RSI ({tf})", cur['rsi']) # Dynamiczne RSI w metryce

    components.html(f"""
        <div style="height:380px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf}", "width": "100%", "isTransparent": true, "height": 380,
            "symbol": "{cur['sym']}", "showIntervalTabs": false, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=400)
