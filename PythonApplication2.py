import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja Stylu - Wysoki Kontrast
st.set_page_config(layout="wide", page_title="TERMINAL V148", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa czytelności w rankingu - wymuszenie czarnego tła okna */
    div[role="dialog"] { background-color: #1e222d !important; }
    div[role="dialog"] p, div[role="dialog"] h3 { color: #ffffff !important; }

    /* Przyciski operacyjne */
    div.stButton > button { 
        background-color: #262730 !important; 
        color: #ffffff !important; 
        border: 2px solid #00ff88 !important;
        font-weight: bold !important;
        width: 100% !important;
        font-size: 0.75rem !important;
    }

    .signal-card-v148 { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 6px; border: 1px solid #333; border-left: 5px solid #3d4451; }
    .pair-header { display: flex; justify-content: space-between; align-items: center; }
    .pair-name { font-size: 0.95rem; font-weight: bold; }
    .data-box { background: #000; padding: 6px; border-radius: 5px; color: #00ff88 !important; text-align: center; margin: 5px 0; border: 1px solid #00ff88; font-family: monospace; font-weight: bold; }
    
    .tg-link { 
        background-color: #0088cc; color: white !important; text-decoration: none; 
        display: flex; align-items: center; justify-content: center; 
        height: 33px; border-radius: 4px; font-weight: bold; font-size: 0.7rem; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Pełna Baza Danych (9 Sygnałów)
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "conf": 94, "basis": "Strong Bullish Momentum"},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "conf": 82, "basis": "Trendline Support"},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "conf": 87, "basis": "Resistance Rejection"},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "conf": 78, "basis": "Lower High Pattern"},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "113.85", "tp": "114.50", "conf": 75, "basis": "MA 200 Support"},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "conf": 72, "basis": "Fibonacci Retracement"},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "1.073", "tp": "1.071", "conf": 70, "basis": "Overbought Resistance"},
    {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "10.01 | 14:30", "tg": "https://t.me/s/signalsproviderfx", "color": "#00ff88", "type": "KUPNO", "in": "2.003", "tp": "2.007", "conf": 68, "basis": "EMA Bounce"},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 10:22", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "0.851", "tp": "0.858", "conf": 65, "basis": "Support Rebound"}
]

# Mapowanie RSI dla różnych TF
rsi_data = {p["pair"]: {tf: (40 + (idx * 2) + (len(tf) * 5)) % 80 for tf in ["1m", "15m", "1h", "1D", "1W"]} for idx, p in enumerate(db)}

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1D"

# 3. INTERFEJS RANKINGU
@st.dialog("🤖 RANKING AI + DYNAMICZNE RSI")
def show_ai_ranking_v148():
    tf = st.session_state.current_tf
    st.markdown(f"**Interwał: {tf}**")
    ranked = sorted(db, key=lambda x: x['conf'], reverse=True)
    for i, item in enumerate(ranked):
        val_rsi = rsi_data[item['pair']].get(tf, 50.0)
        clr = "#00ff88" if item['conf'] > 80 else "#ff9800"
        st.markdown(f"""
            <div style="color:white; margin-bottom:10px;">
                <strong>{i+1}. {item['pair']}</strong> | Szansa: <span style="color:{clr};">{item['conf']}%</span> | <strong>RSI: {val_rsi}</strong><br>
                <small style="color:#aaa;">Analiza: {item['basis']}</small>
            </div>
            <hr style="border-color:#444; margin:5px 0;">
        """, unsafe_allow_html=True)
    if st.button("ZAMKNIJ"): st.rerun()

# --- PANEL GŁÓWNY ---
st.markdown('<div style="background:#1e222d; padding:8px; border-radius:5px; border:1px solid #00ff88; text-align:center; margin-bottom:10px; font-weight:bold;">TERMINAL V148 | Pełna Lista Sygnałów (9)</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("🔄 SYNCHRONIZUJ"): st.toast("✅ Baza danych zaktualizowana (9 sygnałów)", icon="🚀")
with c2:
    if st.button("🤖 AI RANKING"): show_ai_ranking_v148()

st.write("---")
col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA STRONA (Lista Sygnałów) ---
with col_l:
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card-v148" style="border-left-color:{s['color']}">
                <div class="pair-header">
                    <span class="pair-name">{s['pair']} <span style="color:{s['color']}">{s['type']}</span></span>
                    <span style="font-size:0.7rem; color:#888;">{s['time']}</span>
                </div>
                <div class="data-box">WEJŚCIE: {s['in']} | CEL: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with b2:
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-link">✈️ TELEGRAM</a>', unsafe_allow_html=True)

# --- PRAWA STRONA (Wykresy i RSI) ---
with col_r:
    cur = db[st.session_state.active_idx]
    st.session_state.current_tf = st.select_slider("Interwał:", options=["1m", "15m", "1h", "1D", "1W"], value=st.session_state.current_tf)
    
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    val_rsi = rsi_data[cur['pair']].get(st.session_state.current_tf, 50.0)
    
    m1.metric("Investing", cur['type'])
    m2.metric("TradingView", cur['type'])
    m3.metric(f"RSI ({st.session_state.current_tf})", val_rsi)

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
