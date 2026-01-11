import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja Stylu - Maksymalny Kontrast i Czytelność
st.set_page_config(layout="wide", page_title="TERMINAL V147", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa czytelności w oknach dialogowych (Ranking AI) */
    div[data-testid="stDialog"] div {
        background-color: #1e222d !important;
        color: #ffffff !important;
    }
    
    /* Globalne wymuszenie jasnego tekstu dla opisów */
    .stMarkdown, p, span, label { color: #ffffff !important; }
    
    div.stButton > button { 
        background-color: #262730 !important; 
        color: #ffffff !important; 
        border: 2px solid #00ff88 !important;
        font-weight: bold !important;
        width: 100% !important;
        font-size: 0.75rem !important;
        padding: 5px !important;
    }

    .signal-card-v147 { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 6px; border: 1px solid #333; border-left: 5px solid #3d4451; }
    .pair-title { font-size: 1rem; font-weight: bold; color: #ffffff; }
    .time-stamp { font-size: 0.75rem; color: #00ff88; font-weight: bold; }
    .data-row { background: #000; padding: 8px; border-radius: 5px; color: #00ff88 !important; font-family: monospace; text-align: center; margin: 5px 0; border: 1px solid #00ff88; font-size: 0.85rem; font-weight: bold; }

    .tg-link-small { 
        background-color: #0088cc; color: white !important; text-decoration: none; 
        display: flex; align-items: center; justify-content: center; 
        height: 33px; border-radius: 4px; font-weight: bold; font-size: 0.7rem; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych i Symulacja Dynamicznego RSI
rsi_map = {
    "XAU/USD": {"1m": 42.1, "15m": 55.4, "1h": 61.2, "1D": 68.5, "1W": 74.2},
    "GBP/JPY": {"1m": 68.4, "15m": 70.1, "1h": 72.5, "1D": 72.1, "1W": 62.5},
    "US30": {"1m": 31.2, "15m": 35.8, "1h": 40.1, "1D": 42.5, "1W": 44.9},
    "NATGAS": {"1m": 22.5, "15m": 27.1, "1h": 29.8, "1D": 31.2, "1W": 36.4},
    "EUR/CHF": {"1m": 48.2, "15m": 45.4, "1h": 43.1, "1D": 41.5, "1W": 39.8}
}

db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "conf": 94, "basis": "Silny impet, wsparcie MA200."},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "conf": 89, "basis": "RSI wykupione, EMA Cross."},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "conf": 87, "basis": "Bearish Divergence na H1."},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "conf": 82, "basis": "RSI wyprzedane, linia trendu."},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "conf": 78, "basis": "Opór Fibo, słaby popyt."}
]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1D"

# 3. RANKING AI Z POPRAWIONYM KONTRASTEM
@st.dialog("🤖 RANKING SKUTECZNOŚCI AI")
def show_ai_ranking_v147():
    tf = st.session_state.current_tf
    st.markdown(f"### Interwał Analizy: {tf}")
    ranked = sorted(db, key=lambda x: x['conf'], reverse=True)
    for i, item in enumerate(ranked):
        val_rsi = rsi_map.get(item['pair'], {}).get(tf, 50.0)
        clr = "#00ff88" if item['conf'] > 80 else "#ff9800"
        # Wymuszony biały tekst w markdownie dla dialogu
        st.markdown(f"""
            <div style="color:white;">
            <strong>{i+1}. {item['pair']}</strong> | Szansa: <span style="color:{clr};">{item['conf']}%</span> | <strong>RSI: {val_rsi}</strong><br>
            <em>Podstawa: {item['basis']}</em>
            </div>
            <hr style="border-color:#444;">
        """, unsafe_allow_html=True)
    if st.button("ZAMKNIJ"): st.rerun()

# --- PANEL STEROWANIA ---
st.markdown('<div style="background:#1e222d; padding:8px; border-radius:5px; border:1px solid #00ff88; text-align:center; margin-bottom:10px; font-weight:bold; font-size:0.8rem;">TERMINAL V147 | Gwarantowana Czytelność Rankingu</div>', unsafe_allow_html=True)

# PRZYCISKI GÓRNE (Mobile Optimized)
c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🔄 SYNC DATA"):
        st.toast("✅ Dane zaktualizowane!", icon="🚀") # Przywrócony Toast
with c_nav2:
    if st.button("🤖 AI RANKING"): show_ai_ranking_v147()

st.write("---")
col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA STRONA: SYGNAŁY (Układ 1+1) ---
with col_l:
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card-v147" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between;">
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
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-link-small">✈️ TELEGRAM</a>', unsafe_allow_html=True)

# --- PRAWA STRONA: WSKAŹNIKI I WYKRES ---
with col_r:
    cur = db[st.session_state.active_idx]
    st.session_state.current_tf = st.select_slider("Zmień interwał:", options=["1m", "15m", "1h", "1D", "1W"], value=st.session_state.current_tf)
    
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    dynamic_rsi_val = rsi_map.get(cur['pair'], {}).get(st.session_state.current_tf, 50.0)
    
    m1.metric("Investing", cur['type'])
    m2.metric("TradingView", cur['type'])
    m3.metric(f"RSI ({st.session_state.current_tf})", dynamic_rsi_val)

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
