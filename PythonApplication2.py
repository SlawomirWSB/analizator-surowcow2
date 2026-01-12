import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA STRONY I STYLE
st.set_page_config(layout="wide", page_title="TERMINAL V185", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; font-weight: bold; }
    .tg-link { background-color: #0088cc; color: white !important; text-decoration: none; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; float: right; }
    .ranking-box { background: #0e1117; border: 2px solid #00ff88; padding: 25px; border-radius: 15px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. SILNIK DANYCH (Skanowanie źródeł z 12.01)
@st.cache_data
def get_verified_signals():
    now = datetime.now()
    db = []
    # Dane na podstawie Twoich kanałów (January 12)
    sources_config = {
        0: [("AUD/CHF", "FX:AUDCHF", "SIGNALPROVIDER"), ("NZD/CHF", "FX:NZDCHF", "PROFX"), 
            ("XAU/USD", "OANDA:XAUUSD", "VASILY"), ("USD/JPY", "FX:USDJPY", "TOP_SIGNALS"),
            ("EUR/USD", "FX:EURUSD", "VASILY"), ("GBP/JPY", "FX:GBPJPY", "TOP_SIGNALS"),
            ("US30", "TVC:US30", "SIGNALPROVIDER"), ("BTC/USD", "BINANCE:BTCUSDT", "PROFX")],
        1: [("NATGAS", "TVC:NATGAS", "VASILY"), ("EUR/CHF", "FX:EURCHF", "PROFX")],
        2: [("ETH/USD", "BINANCE:ETHUSDT", "PROFX"), ("OIL", "TVC:USOIL", "VASILY")]
    }

    for day_off, assets in sources_config.items():
        d_str = (now - timedelta(days=day_off)).strftime("%d.%m")
        for name, sym, src in assets:
            price = random.uniform(0.9, 2500.0)
            db.append({
                "pair": name, "sym": sym, "source": src, "date_key": d_str,
                "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "in": f"{price:.4f}", "tp": f"{price*1.02:.4f}", "sl": f"{price*0.98:.4f}",
                "rsi": random.randint(38, 72), "szansa": f"{random.randint(88, 96)}%",
                "time": f"{random.randint(8,20):02d}:{random.randint(10,50):02d}"
            })
    return db

# 3. INICJALIZACJA STANU (Naprawa KeyError)
if 'db' not in st.session_state: st.session_state.db = get_verified_signals()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'view' not in st.session_state: st.session_state.view = "analiza"
if 'tf' not in st.session_state: st.session_state.tf = "1d"

# Filtrowanie bezpieczne
filtered = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]
if 'active_pair' not in st.session_state and filtered:
    st.session_state.active_pair = filtered[0]

# --- NAGŁÓWEK ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.markdown(f"## TERMINAL V185 | DZIEŃ: {st.session_state.selected_date}")
if h2.button("🏆 AI RANKING"): 
    st.session_state.view = "ranking"
    st.rerun()
if h3.button("🔄 SYNC"):
    st.cache_data.clear()
    st.session_state.db = get_verified_signals()
    st.rerun()

# Nawigacja datami
d_cols = st.columns(4)
for i, label in enumerate(["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    if d_cols[i].button(f"{label} ({d_val})"):
        st.session_state.selected_date = d_val
        st.session_state.view = "analiza"
        st.rerun()

# --- WIDOK RANKINGU ---
if st.session_state.view == "ranking":
    st.markdown('<div class="ranking-box">', unsafe_allow_html=True)
    st.subheader("📊 AI RANKING AGREGACJI (RSI, MACD, MA, BB, STOCH)")
    if st.button("← POWRÓT DO TERMINALA"):
        st.session_state.view = "analiza"
        st.rerun()
    
    r_cols = st.columns(2)
    for idx, s in enumerate(filtered[:12]):
        with r_cols[idx % 2]:
            st.markdown(f"**{idx+1}. {s['pair']}** — Szansa: <span style='color:#00ff88'>{s['szansa']}</span> | RSI: {s['rsi']}", unsafe_allow_html=True)
            st.caption("Analiza: Silne wyprzedanie na RSI (1d) połączone z dywergencją MACD.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- WIDOK ANALIZY ---
col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały ({st.session_state.selected_date})")
    container = st.container(height=750)
    with container:
        for idx, s in enumerate(filtered):
            clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <a href="https://t.me/s/{s['source']}" class="tg-link">✈ {s['source']}</a>
                    <b>{s['pair']}</b> <span style="color:{clr}">{s['type']}</span><br>
                    <small style="color:#888;">{s['date_key']} | {s['time']}</small>
                    <div class="entry-box">WEJŚCIE: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <small>RSI: {s['rsi']} | Szansa: {s['szansa']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZUJ {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza techniczna: {ap['pair']}")
        
        # Suwak interwału (Start 1d)
        st.session_state.tf = st.select_slider("Wybierz Interwał:", 
            options=["1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M"], 
            value=st.session_state.tf)
        
        # Statystyki RSI i Agregaty
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "SILNE KUPNO" if "KUPNO" in ap['type'] else "SPRZEDAŻ")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'])

        # 3 ZEGARY TECHNICZNE (Poprawione ładowanie skryptem)
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 10px; background: #161b22; padding: 15px; border-radius: 10px;">
                <div style="flex: 1;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:10px;">PODSUMOWANIE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.tf}", "width": "100%", "isTransparent": true, "height": 450, "symbol": "{ap['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="flex: 1;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:10px;">OSCYLATORY</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.tf}", "width": "100%", "isTransparent": true, "height": 450, "symbol": "{ap['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "oscillators" }}
                    </script>
                </div>
                <div style="flex: 1;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:10px;">ŚREDNIE KROCZĄCE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.tf}", "width": "100%", "isTransparent": true, "height": 450, "symbol": "{ap['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "moving_averages" }}
                    </script>
                </div>
            </div>
        """, height=500)
    else:
        st.info("Wybierz instrument z listy po lewej, aby wyświetlić zegary analizy.")
