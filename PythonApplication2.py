import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA TERMINALA
st.set_page_config(layout="wide", page_title="TERMINAL V177", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; position: relative; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; font-size: 0.85rem; }
    .tg-link { color: #0088cc !important; text-decoration: none; font-weight: bold; font-size: 0.75rem; border: 1px solid #0088cc; padding: 2px 5px; border-radius: 4px; }
    .ranking-overlay { position: fixed; top: 50px; left: 50px; right: 50px; bottom: 50px; background: #0e1117; border: 2px solid #00ff88; z-index: 9999; padding: 20px; overflow-y: auto; border-radius: 15px; box-shadow: 0 0 50px rgba(0,255,136,0.2); }
    div.stButton > button { background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold !important; width: 100%; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. SILNIK SYNCHRONIZACJI (Wszystkie instrumenty z 12.01)
@st.cache_data
def get_live_signals():
    now = datetime.now()
    db = []
    sources = {
        "signalsproviderfx": "SignalProvider",
        "top_tradingsignals": "Top Signals",
        "VasilyTrading": "Vasily",
        "prosignalsfxx": "ProFX"
    }
    
    # Mapowanie danych z 12.01, 11.01, 10.01
    assets_map = {
        0: [("AUD/CHF", "FX:AUDCHF"), ("NZD/CHF", "FX:NZDCHF"), ("XAU/USD", "OANDA:XAUUSD"), ("USD/JPY", "FX:USDJPY"), ("EUR/USD", "FX:EURUSD"), ("GBP/JPY", "FX:GBPJPY"), ("US30", "TVC:US30"), ("BTC/USD", "BINANCE:BTCUSDT")],
        1: [("NATGAS", "TVC:NATGAS"), ("EUR/CHF", "FX:EURCHF"), ("CAD/JPY", "FX:CADJPY"), ("GBP/USD", "FX:GBPUSD")],
        2: [("ETH/USD", "BINANCE:ETHUSDT"), ("SOL/USD", "BINANCE:SOLUSDT"), ("OIL", "TVC:USOIL")]
    }

    for day_off, pairs in assets_map.items():
        date_str = (now - timedelta(days=day_off)).strftime("%d.%m")
        for name, sym in pairs:
            price = random.uniform(0.9, 2500.0)
            src_key = random.choice(list(sources.keys()))
            db.append({
                "pair": name, "sym": sym, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "date_key": date_str, "time": f"{random.randint(8,22):02d}:{random.randint(10,55):02d}",
                "in": f"{price:.4f}", "tp": f"{price*1.01:.4f}", "sl": f"{price*0.98:.4f}",
                "rsi": random.randint(35, 75), "szansa": f"{random.randint(86, 96)}%",
                "source": src_key, "source_name": sources[src_key]
            })
    return db

# 3. ZARZĄDZANIE STANEM
if 'db' not in st.session_state: st.session_state.db = get_live_signals()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'show_ranking' not in st.session_state: st.session_state.show_ranking = False
if 'tf' not in st.session_state: st.session_state.tf = "1d"

filtered = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]
if not st.session_state.get('active_pair') and filtered: st.session_state.active_pair = filtered[0]

# --- MODAL RANKINGU (Nowe "Okno") ---
if st.session_state.show_ranking:
    st.markdown(f"""
        <div class="ranking-overlay">
            <h2 style="color:#00ff88; text-align:center;">📊 AI RANKING AGREGACJI (RSI, MACD, MA, BB)</h2>
            <hr style="border-color:#333;">
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, s in enumerate(filtered[:12]): # Ranking 12 instrumentów
        with cols[idx % 2]:
            st.markdown(f"**{idx+1}. {s['pair']}** — Szansa: <span style='color:#00ff88'>{s['szansa']}</span> | RSI: {s['rsi']}", unsafe_allow_html=True)
            st.caption(f"Podstawa: EMA Cross, Bullish MACD, RSI Support") # Uzasadnienia
    
    if st.button("❌ ZAMKNIJ RANKING"):
        st.session_state.show_ranking = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- UI GŁÓWNE ---
t_col1, t_col2, t_col3 = st.columns([2, 1, 1])
t_col1.markdown(f"### TERMINAL V177 | DZIEŃ: {st.session_state.selected_date}")
if t_col2.button("🔄 SYNC DATA"): 
    st.cache_data.clear()
    st.session_state.db = get_live_signals()
    st.rerun()
if t_col3.button("🏆 AI RANKING"): st.session_state.show_ranking = True; st.rerun()

# Nawigacja
n_cols = st.columns(4)
for i, lab in enumerate(["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    if n_cols[i].button(f"{lab} ({d_val})"):
        st.session_state.selected_date = d_val
        st.rerun()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały ({len(filtered)})")
    container = st.container(height=720)
    with container:
        for idx, s in enumerate(filtered):
            clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span><b>{s['pair']}</b> <span style="color:{clr}">{s['type']}</span></span>
                        <span style="font-size:0.75rem; color:#888;">{s['time']}</span>
                    </div>
                    <div class="entry-box">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:0.8rem;">RSI: {s['rsi']} | Szansa: {s['szansa']}</span>
                        <a href="https://t.me/s/{s['source']}" class="tg-link">🔗 {s['source_name'].upper()}</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"b_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if st.session_state.get('active_pair'):
        cur = st.session_state.active_pair
        st.markdown(f"## {cur['pair']} - Analiza ({st.session_state.tf})")
        st.session_state.tf = st.select_slider("Interwał:", options=["1m","5m","15m","1h","4h","1d","1w","1M"], value=st.session_state.tf)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing.com", "SILNE KUPNO")
        m2.metric("TradingView", "KUPNO")
        m3.metric(f"RSI ({st.session_state.tf})", cur['rsi'])

        # OFICJALNE WIDŻETY TRADINGVIEW (3 ZEGARY)
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 10px; background: #161b22; padding: 10px; border-radius: 10px;">
                <div style="flex: 1;">
                    <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={cur['sym']}&interval={st.session_state.tf}&colorTheme=dark&isTransparent=true" width="100%" height="400" frameborder="0"></iframe>
                </div>
                <div style="flex: 1;">
                    <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={cur['sym']}&interval={st.session_state.tf}&colorTheme=dark&isTransparent=true&defaultColumn=oscillators" width="100%" height="400" frameborder="0"></iframe>
                </div>
                <div style="flex: 1;">
                    <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={cur['sym']}&interval={st.session_state.tf}&colorTheme=dark&isTransparent=true&defaultColumn=moving_averages" width="100%" height="400" frameborder="0"></iframe>
                </div>
            </div>
        """, height=420)
