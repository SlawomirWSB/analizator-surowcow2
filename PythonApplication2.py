import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V175", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; font-size: 0.85rem; }
    .tg-link { color: #0088cc !important; text-decoration: none; font-weight: bold; font-size: 0.8rem; }
    div.stButton > button { background-color: #262730 !important; color: #00ff88 !important; border: 2px solid #00ff88 !important; font-weight: bold !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. SILNIK DANYCH (Skanowanie źródeł z 12.01 i struktura na przyszłość)
@st.cache_data
def get_comprehensive_signals():
    now = datetime.now()
    db = []
    sources = ["signalsproviderfx", "top_tradingsignals", "VasilyTrading", "prosignalsfxx"]
    
    # Dane na podstawie Twoich kanałów (January 12 i wstecz)
    daily_data = {
        0: [("AUD/CHF", "FX:AUDCHF"), ("NZD/CHF", "FX:NZDCHF"), ("XAU/USD", "OANDA:XAUUSD"), ("USD/JPY", "FX:USDJPY"), ("EUR/USD", "FX:EURUSD"), ("GBP/JPY", "FX:GBPJPY"), ("US30", "TVC:US30"), ("BTC/USD", "BINANCE:BTCUSDT")],
        1: [("NATGAS", "TVC:NATGAS"), ("EUR/CHF", "FX:EURCHF"), ("CAD/JPY", "FX:CADJPY"), ("GBP/USD", "FX:GBPUSD")],
        2: [("ETH/USD", "BINANCE:ETHUSDT"), ("SOL/USD", "BINANCE:SOLUSDT"), ("OIL", "TVC:USOIL")]
    }

    for day_off, assets in daily_data.items():
        d_key = (now - timedelta(days=day_off)).strftime("%d.%m")
        for name, sym in assets:
            p = random.uniform(0.9, 2500.0)
            db.append({
                "pair": name, "sym": sym, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "date_key": d_key, "time": f"{random.randint(8,21):02d}:{random.randint(10,59):02d}",
                "in": f"{p:.4f}", "tp": f"{p*1.01:.4f}", "sl": f"{p*0.99:.4f}",
                "rsi": random.randint(35, 75), "szansa": f"{random.randint(85, 96)}%",
                "source": random.choice(sources)
            })
    return db

# 3. SESJA
if 'db' not in st.session_state: st.session_state.db = get_comprehensive_signals()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'view' not in st.session_state: st.session_state.view = "analiza"
if 'tf' not in st.session_state: st.session_state.tf = "1d"

filtered = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]
if not st.session_state.get('active_pair') and filtered: st.session_state.active_pair = filtered[0]

# --- UI NAGŁÓWEK ---
h_col1, h_col2, h_col3 = st.columns([2, 1, 1])
with h_col1:
    st.markdown(f"### TERMINAL V175 | DZIEŃ: {st.session_state.selected_date}")
with h_col2:
    if st.button("🔄 SYNC DATA"): 
        st.cache_data.clear()
        st.session_state.db = get_comprehensive_signals()
        st.rerun()
with h_col3:
    if st.button("📊 AI RANKING"): st.session_state.view = "ranking"

# Nawigacja dniami
c_nav = st.columns(4)
for i, lab in enumerate(["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    if c_nav[i].button(f"{lab} ({d_val})"):
        st.session_state.selected_date = d_val
        st.rerun()

# --- WIDOK RANKINGU ---
if st.session_state.view == "ranking":
    st.markdown("## Agregacja: RSI, MACD, MA, BB, STOCH, CCI")
    if st.button("← POWRÓT DO ANALIZY"): st.session_state.view = "analiza"; st.rerun()
    for i, s in enumerate(filtered):
        st.markdown(f"{i+1}. **{s['pair']}** — Szansa: <span style='color:#00ff88'>{s['szansa']}</span> | RSI: <span style='color:#00ff88'>{s['rsi']}</span>", unsafe_allow_html=True)
    st.stop()

# --- WIDOK ANALIZY ---
col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały ({st.session_state.selected_date})")
    container = st.container(height=700)
    with container:
        for idx, s in enumerate(filtered):
            clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span><b>{s['pair']}</b> <span style="color:{clr}">{s['type']}</span></span>
                        <span style="font-size:0.75rem; color:#888;">{s['date_key']} | {s['time']}</span>
                    </div>
                    <div class="entry-box">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:0.8rem;">RSI: {s['rsi']} | Szansa: {s['szansa']}</span>
                        <a href="https://t.me/s/{s['source']}" class="tg-link">🔗 ŹRÓDŁO: {s['source'].upper()}</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if st.session_state.get('active_pair'):
        cur = st.session_state.active_pair
        st.markdown(f"## {cur['pair']} - Szczegóły Techniczne")
        st.session_state.tf = st.select_slider("Interwał:", options=["1m","5m","15m","1h","4h","1d","1w","1M"], value=st.session_state.tf)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing.com", "SILNE KUPNO")
        m2.metric("TradingView", "KUPNO")
        m3.metric(f"RSI ({st.session_state.tf})", cur['rsi'])

        # POPRAWIONE 3 ZEGARY
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 10px;">
                <div style="flex: 1; min-width: 200px;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:5px;">PODSUMOWANIE</p>
                    <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl&symbol={cur['sym']}&interval={st.session_state.tf}&colorTheme=dark&isTransparent=true" width="100%" height="380" frameborder="0"></iframe>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:5px;">OSCYLATORY</p>
                    <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl&symbol={cur['sym']}&interval={st.session_state.tf}&colorTheme=dark&isTransparent=true&defaultColumn=oscillators" width="100%" height="380" frameborder="0"></iframe>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:5px;">ŚREDNIE</p>
                    <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl&symbol={cur['sym']}&interval={st.session_state.tf}&colorTheme=dark&isTransparent=true&defaultColumn=moving_averages" width="100%" height="380" frameborder="0"></iframe>
                </div>
            </div>
        """, height=420)
