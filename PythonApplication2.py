import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Zaawansowany CSS dla Mobile
st.set_page_config(layout="wide", page_title="TERMINAL V144", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* GWARANTOWANA WIDOCZNOŚĆ I ROZMIAR PRZYCISKÓW */
    div.stButton > button { 
        background-color: #262730 !important; 
        color: #ffffff !important; 
        border: 1px solid #00ff88 !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 5px 2px !important; /* Zmniejszony padding dla oszczędności miejsca */
        font-size: 0.75rem !important;
    }

    /* Karta instrumentu */
    .signal-card-v144 { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 5px solid #3d4451; }
    .card-top { display: flex; justify-content: space-between; align-items: center; }
    .pair-title { font-size: 0.95rem; font-weight: bold; }
    .time-stamp { font-size: 0.7rem; color: #00ff88; }
    .data-row { background: #000; padding: 6px; border-radius: 5px; color: #00ff88; font-family: monospace; text-align: center; margin: 5px 0; border: 1px solid #333; font-size: 0.85rem; }

    /* STYL PRZYCISKU TELEGRAM (ZMNIEJSZONY) */
    .tg-link-small { 
        background-color: #0088cc; 
        color: white !important; 
        text-decoration: none; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        height: 33px; 
        border-radius: 4px; 
        font-weight: bold; 
        font-size: 0.7rem; 
        border: 1px solid #4b4d5a; 
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych (Analiza wielowskaźnikowa PL)
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "conf": 94, "basis": "Silny impet wzrostowy, wsparcie MA200, RSI bycze."},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "conf": 89, "basis": "RSI wykupione, EMA Cross, odrzucenie oporu 211.70."},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "conf": 87, "basis": "Odrzucenie oporu, niedźwiedzia dywergencja na H1."},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "conf": 82, "basis": "Linia trendu wzrostowego, RSI wyprzedane na H4."},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "conf": 78, "basis": "Struktura niższych szczytów, opór Fibonacciego."},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "113.85", "tp": "114.50", "conf": 75, "basis": "Wsparcie MA 200, akumulacja wolumenu."},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "conf": 72, "basis": "Zniesienie Fibo 0.618, Price Action na oporze."}
]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0

# 3. OKNO RANKINGU AI PO POLSKU
@st.dialog("🤖 RANKING AI (PL)")
def show_ai_ranking_pl():
    ranked = sorted(db, key=lambda x: x['conf'], reverse=True)
    for i, item in enumerate(ranked):
        clr = "#00ff88" if item['conf'] > 80 else "#ff9800"
        st.markdown(f"**{i+1}. {item['pair']}** | <span style='color:{clr};'>{item['conf']}%</span>\n\n*{item['basis']}*\n---", unsafe_allow_html=True)
    if st.button("ZAMKNIJ"): st.rerun()

# --- NAGŁÓWEK ---
st.markdown('<div style="background:#1e222d; padding:8px; border-radius:5px; border:1px solid #00ff88; text-align:center; margin-bottom:10px; font-size:0.8rem;">TERMINAL V144 | 11.01.2026 | Mobile Optimized</div>', unsafe_allow_html=True)

# GÓRNY WIERSZ: SYNC + AI
c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🔄 SYNC"): st.success("OK")
with c_nav2:
    if st.button("🤖 AI RANK"): show_ai_ranking_pl()

st.write("---")
col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA STRONA: SYGNAŁY (2 KOLUMNY PRZYCISKÓW) ---
with col_l:
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card-v144" style="border-left-color:{s['color']}">
                <div class="card-top">
                    <span class="pair-title">{s['pair']} <span style="color:{s['color']}">{s['type']}</span></span>
                    <span class="time-stamp">{s['time']}</span>
                </div>
                <div class="data-row">WEJ: {s['in']} | CEL: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # JEDEN WIERSZ NA MOBILE
        btn_c1, btn_c2 = st.columns([1, 1])
        with btn_c1:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with btn_c2:
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-link-small">✈️ TG</a>', unsafe_allow_html=True)

# --- PRAWA STRONA: 3 ZEGAREK ---
with col_r:
    cur = db[st.session_state.active_idx]
    tf = st.select_slider("TF:", options=["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"], value="1D")
    
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Invest", cur['type'])
    m2.metric("TV", cur['type'])
    m3.metric("AI", f"{cur['conf']}%")

    components.html(f"""
        <div style="height:400px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf}", "width": "100%", "isTransparent": true, "height": 400,
            "symbol": "{cur['sym']}", "showIntervalTabs": false, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=420)
