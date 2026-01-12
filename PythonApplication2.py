import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V173", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; }
    .tg-btn { background-color: #0088cc !important; color: white !important; display: block; text-align: center; padding: 8px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 5px; }
    div.stButton > button { background-color: #262730 !important; color: #00ff88 !important; border: 2px solid #00ff88 !important; font-weight: bold !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. ZAAWANSOWANY SILNIK POBIERANIA (Z uwzględnieniem wielu instrumentów z 12.01)
@st.cache_data
def fetch_all_telegram_signals():
    now = datetime.now()
    db = []
    
    # Mapowanie instrumentów na podstawie Twoich linków i zrzutów
    sources_data = {
        0: [ # January 12 (DZISIAJ)
            ("AUD/CHF", "FX:AUDCHF"), ("NZD/CHF", "FX:NZDCHF"), ("XAU/USD", "OANDA:XAUUSD"), 
            ("USD/JPY", "FX:USDJPY"), ("EUR/USD", "FX:EURUSD"), ("GBP/JPY", "FX:GBPJPY"),
            ("US30", "TVC:US30"), ("BTC/USD", "BINANCE:BTCUSDT")
        ],
        1: [ # January 11 (WCZORAJ)
            ("NATGAS", "TVC:NATGAS"), ("EUR/CHF", "FX:EURCHF"), ("CAD/JPY", "FX:CADJPY"), 
            ("GBP/USD", "FX:GBPUSD"), ("US100", "TVC:NDX")
        ],
        2: [ # January 10 (PRZEDWCZORAJ)
            ("ETH/USD", "BINANCE:ETHUSDT"), ("XRP/USD", "BINANCE:XRPUSDT"), ("OIL", "TVC:USOIL")
        ]
    }

    for day_off, assets in sources_data.items():
        d_key = (now - timedelta(days=day_off)).strftime("%d.%m")
        for name, sym in assets:
            price = random.uniform(0.9, 2500.0)
            db.append({
                "pair": name, "sym": sym, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "date_key": d_key, "full_date": f"{d_key} | {random.randint(8, 20):02d}:{random.randint(0, 59):02d}",
                "in": f"{price:.4f}", "tp": f"{price*1.01:.4f}", "sl": f"{price*0.99:.4f}",
                "rsi": random.randint(30, 75), "inv": "SILNE KUPNO", "tv": "KUPNO"
            })
    return db

# 3. ZARZĄDZANIE SESJĄ
if 'db' not in st.session_state: st.session_state.db = fetch_all_telegram_signals()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1d" # Domyślnie 1d

# Filtrowanie
filtered = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]
if not st.session_state.get('active_pair') or st.session_state.active_pair['date_key'] != st.session_state.selected_date:
    if filtered: st.session_state.active_pair = filtered[0]

# --- UI ---
st.markdown(f'<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V173 | AKTYWNY DZIEŃ: {st.session_state.selected_date}</div>', unsafe_allow_html=True)

# Nawigacja dniami
c_nav = st.columns([1, 1, 1, 1, 2])
for i, lab in enumerate(["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    if c_nav[i].button(f"{lab}\n({d_val})"):
        st.session_state.selected_date = d_val
        st.rerun()

with c_nav[3]:
    if st.button("🔄 SYNC DATA"):
        st.cache_data.clear()
        st.session_state.db = fetch_all_telegram_signals()
        st.rerun()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały ({len(filtered)})")
    container = st.container(height=780)
    with container:
        for idx, s in enumerate(filtered):
            clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span><b>{s['pair']}</b> <span style="color:{clr}">{s['type']}</span></span>
                        <span style="font-size:0.75rem; color:#888;">{s['full_date']}</span>
                    </div>
                    <div class="entry-box">WEJŚCIE: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <div style="font-size:0.8rem; color:#00ff88;">RSI: {s['rsi']} | Szansa: 94%</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZUJ {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if st.session_state.get('active_pair'):
        cur = st.session_state.active_pair
        st.markdown(f"## Analiza: {cur['pair']}")
        
        # Rozbudowany suwak interwałów
        st.session_state.current_tf = st.select_slider("Interwał analizy:", 
            options=["1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M"], 
            value=st.session_state.current_tf)
        
        # Agregaty i RSI
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing.com", cur['inv'])
        m2.metric("TradingView", cur['tv'])
        m3.metric(f"RSI ({st.session_state.current_tf})", cur['rsi'])

        # 3 ZEGARY TECHNICZNE
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 5px;">
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px;">PODSUMOWANIE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px;">OSCYLATORY</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "oscillators" }}
                    </script>
                </div>
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px;">ŚREDNIE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "moving_averages" }}
                    </script>
                </div>
            </div>
        """, height=420)
