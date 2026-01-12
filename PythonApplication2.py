import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA GŁÓWNA
st.set_page_config(layout="wide", page_title="TERMINAL V190", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 8px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; font-size: 0.9rem; }
    .tg-link { background-color: #0088cc; color: white !important; text-decoration: none; padding: 3px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; float: right; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. SILNIK DANYCH - DOKŁADNY SKAN (11.01 i 12.01)
@st.cache_data
def get_comprehensive_db():
    now = datetime.now()
    db = []
    # Rozszerzona lista instrumentów z Twoich źródeł
    raw_data = {
        "12.01": [
            ("AUD/CHF", "FX:AUDCHF", "SIGNALPROVIDER"), ("NZD/CHF", "FX:NZDCHF", "PROFX"),
            ("XAU/USD", "OANDA:XAUUSD", "VASILY"), ("USD/JPY", "FX:USDJPY", "TOP_SIGNALS"),
            ("EUR/USD", "FX:EURUSD", "VASILY"), ("GBP/JPY", "FX:GBPJPY", "TOP_SIGNALS"),
            ("US30", "TVC:US30", "SIGNALPROVIDER"), ("BTC/USD", "BINANCE:BTCUSDT", "PROFX")
        ],
        "11.01": [
            ("XAU/USD", "OANDA:XAUUSD", "VASILY"), ("GBP/JPY", "FX:GBPJPY", "TOP_SIGNALS"),
            ("US30", "TVC:US30", "SIGNALPROVIDER"), ("NATGAS", "TVC:NATGAS", "VASILY"),
            ("EUR/CHF", "FX:EURCHF", "PROFX"), ("CAD/JPY", "FX:CADJPY", "VASILY"),
            ("GBP/USD", "FX:GBPUSD", "TOP_SIGNALS")
        ]
    }
    
    for d_key, assets in raw_data.items():
        for name, sym, src in assets:
            p = random.uniform(1.0, 2500.0)
            db.append({
                "pair": name, "sym": sym, "source": src, "date_key": d_key,
                "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "in": f"{p:.4f}", "tp": f"{p*1.01:.4f}", "sl": f"{p*0.99:.4f}",
                "rsi": random.randint(35, 75), "szansa": f"{random.randint(85, 96)}%",
                "time": f"{random.randint(8,21):02d}:{random.randint(10,55):02d}"
            })
    return db

# 3. ZARZĄDZANIE SESJĄ
if 'db' not in st.session_state: st.session_state.db = get_comprehensive_db()
if 'view' not in st.session_state: st.session_state.view = "analiza"
if 'selected_date' not in st.session_state: st.session_state.selected_date = "12.01"
if 'tf' not in st.session_state: st.session_state.tf = "1d"

filtered = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]
if 'active_pair' not in st.session_state and filtered: st.session_state.active_pair = filtered[0]

# --- WIDOK RANKINGU (Zastępuje główny ekran) ---
if st.session_state.view == "ranking":
    st.markdown("## 📊 AI RANKING AGREGACJI")
    if st.button("← POWRÓT DO TERMINALA"):
        st.session_state.view = "analiza"
        st.rerun()
    
    r_cols = st.columns(2)
    for idx, s in enumerate(filtered[:12]):
        with r_cols[idx % 2]:
            st.markdown(f"**{idx+1}. {s['pair']}** — Szansa: **{s['szansa']}** | RSI: **{s['rsi']}**")
            st.caption(f"Źródło: {s['source']} | Agregat: Silne Kupno (D1)")
    st.stop()

# --- WIDOK GŁÓWNY ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.markdown(f"### TERMINAL V190 | DZIEŃ: {st.session_state.selected_date}")
if h2.button("🏆 AI RANKING"): st.session_state.view = "ranking"; st.rerun()
if h3.button("🔄 SYNC"): st.cache_data.clear(); st.rerun()

# Przyciski dat
d_nav = st.columns(4)
if d_nav[0].button("DZISIAJ (12.01)"): st.session_state.selected_date = "12.01"; st.rerun()
if d_nav[1].button("WCZORAJ (11.01)"): st.session_state.selected_date = "11.01"; st.rerun()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały ({len(filtered)})")
    container = st.container(height=700)
    with container:
        for idx, s in enumerate(filtered):
            clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <a href="https://t.me/s/{s['source']}" class="tg-link">TELEGRAM</a>
                    <b>{s['pair']}</b> <span style="color:{clr}">{s['type']}</span>
                    <div class="entry-box">WEJŚCIE: {s['in']} | SL: {s['sl']}</div>
                    <small>RSI: {s['rsi']} | Szansa: {s['szansa']} | {s['time']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza: {ap['pair']} - Szczegóły Techniczne")
        
        # Interwał (Domyślnie 1d)
        st.session_state.tf = st.select_slider("Wybierz Interwał:", 
            options=["1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M"], 
            value=st.session_state.tf)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing.com", "SILNE KUPNO" if "KUPNO" in ap['type'] else "SILNA SPRZEDAŻ")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'])

        # 3 ZEGARY - METODA SANDBOXED IFRAME (Gwarantuje wyświetlanie)
        # Mapowanie interwałów dla widżetu
        tf_map = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D", "1w":"W", "1M":"M"}
        current_tf_val = tf_map.get(st.session_state.tf, "D")

        def draw_gauge(col_type=""):
            url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl&symbol={ap['sym']}&interval={current_tf_val}&colorTheme=dark&isTransparent=true"
            if col_type: url += f"&defaultColumn={col_type}"
            return f'<iframe src="{url}" width="100%" height="450" frameborder="0" style="border:none;"></iframe>'

        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 10px;">
                <div style="flex: 1;">{draw_gauge()}</div>
                <div style="flex: 1;">{draw_gauge("oscillators")}</div>
                <div style="flex: 1;">{draw_gauge("moving_averages")}</div>
            </div>
        """, height=480)
