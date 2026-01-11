import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja Stylu - Maksymalny Kontrast
st.set_page_config(layout="wide", page_title="TERMINAL V146", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa czytelności - Koniec z szarym tekstem */
    .stMarkdown, .stMetric, p, span { color: #ffffff !important; }
    
    div.stButton > button { 
        background-color: #262730 !important; 
        color: #ffffff !important; 
        border: 2px solid #00ff88 !important; /* Grubsza ramka dla widoczności */
        font-weight: bold !important;
        width: 100% !important;
        font-size: 0.75rem !important;
    }

    .signal-card-v146 { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 6px; border: 1px solid #333; border-left: 5px solid #3d4451; }
    .pair-title { font-size: 1rem; font-weight: bold; color: #ffffff; }
    .time-stamp { font-size: 0.75rem; color: #00ff88; font-weight: bold; }
    .data-row { background: #000; padding: 8px; border-radius: 5px; color: #00ff88 !important; font-family: monospace; text-align: center; margin: 5px 0; border: 1px solid #00ff88; font-size: 0.9rem; font-weight: bold; }

    .tg-link { 
        background-color: #0088cc; color: white !important; text-decoration: none; 
        display: flex; align-items: center; justify-content: center; 
        height: 32px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych z dynamicznym mapowaniem RSI
# Symulacja różnych wartości RSI dla różnych interwałów (TF)
rsi_data = {
    "XAU/USD": {"1m": 45.2, "15m": 52.1, "1h": 58.4, "1D": 68.5, "1W": 72.1},
    "GBP/JPY": {"1m": 62.1, "15m": 65.4, "1h": 70.2, "1D": 72.1, "1W": 64.3},
    "US30": {"1m": 35.4, "15m": 38.9, "1h": 41.2, "1D": 42.5, "1W": 45.1},
    "NATGAS": {"1m": 25.1, "15m": 28.4, "1h": 30.5, "1D": 31.2, "1W": 34.8},
    "EUR/CHF": {"1m": 44.2, "15m": 43.1, "1h": 42.5, "1D": 41.5, "1W": 40.2}
}

db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "conf": 94, "basis": "Silny impet, wsparcie MA200."},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "conf": 89, "basis": "EMA Cross, opór horyzontalny."},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "conf": 87, "basis": "Niedźwiedzia dywergencja na oscylatorach."},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "conf": 82, "basis": "Linia trendu, strefa wyprzedania."},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "conf": 78, "basis": "Niższe szczyty, opór Fibonacciego."}
]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1D"

# Funkcja pomocnicza do pobierania RSI
def get_rsi(pair, tf):
    return rsi_data.get(pair, {}).get(tf, 50.0)

# 3. RANKING Z DYNAMICZNYM RSI I POWIADOMIENIA
@st.dialog("🤖 RANKING AI + DYNAMICZNE RSI")
def show_ai_ranking_v146():
    tf = st.session_state.current_tf
    st.write(f"Sygnały dla interwału: **{tf}**")
    ranked = sorted(db, key=lambda x: x['conf'], reverse=True)
    for i, item in enumerate(ranked):
        current_rsi = get_rsi(item['pair'], tf)
        clr = "#00ff88" if item['conf'] > 80 else "#ff9800"
        st.markdown(f"**{i+1}. {item['pair']}** | Szansa: <span style='color:{clr};'>{item['conf']}%</span> | **RSI: {current_rsi}**\n\n*{item['basis']}*\n---", unsafe_allow_html=True)
    if st.button("ZAMKNIJ"): st.rerun()

# --- PANEL GŁÓWNY ---
st.markdown('<div style="background:#1e222d; padding:10px; border-radius:5px; border:1px solid #00ff88; text-align:center; margin-bottom:10px; font-weight:bold;">TERMINAL V146 | Kontrast: WYSOKI | RSI: DYNAMICZNY</div>', unsafe_allow_html=True)

# PRZYCISKI GÓRNE W JEDNEJ LINII
c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🔄 SYNCHRONIZUJ"):
        st.toast("✅ Dane zsynchronizowane pomyślnie!", icon="🚀") # Przywrócone powiadomienie
with c_nav2:
    if st.button("🤖 AI RANKING"): show_ai_ranking_v146()

st.write("---")
col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA STRONA: SYGNAŁY (Wiersz 1+1) ---
with col_l:
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card-v146" style="border-left-color:{s['color']}">
                <div class="card-top">
                    <span class="pair-title">{s['pair']} <span style="color:{s['color']}">{s['type']}</span></span>
                    <span class="time-stamp">{s['time']}</span>
                </div>
                <div class="data-row">WEJŚCIE: {s['in']} | CEL: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with b2:
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-link">✈️ TG</a>', unsafe_allow_html=True)

# --- PRAWA STRONA: DYNAMICZNE RSI I ZEGARY ---
with col_r:
    cur = db[st.session_state.active_idx]
    # Naprawa braku zmian: suwak aktualizuje session_state
    st.session_state.current_tf = st.select_slider("Wybierz interwał (TF):", options=["1m", "15m", "1h", "1D", "1W"], value=st.session_state.current_tf)
    
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    dynamic_rsi = get_rsi(cur['pair'], st.session_state.current_tf) # Dynamiczne pobranie
    
    m1.metric("Investing", cur['type'])
    m2.metric("TradingView", cur['type'])
    m3.metric(f"RSI ({st.session_state.current_tf})", dynamic_rsi)

    # Zegar TradingView
    components.html(f"""
        <div style="height:380px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380,
            "symbol": "{cur['sym']}", "showIntervalTabs": false, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=400)
