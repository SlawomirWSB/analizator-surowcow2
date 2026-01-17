import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random

# ================= CONFIG =================
st.set_page_config(
    layout="wide",
    page_title="TERMINAL V6.1 - LIVE SIGNALS",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%); color: #ffffff; }
div.stButton > button {
    width: 100%; background: linear-gradient(45deg, #00ff88, #00cc6a);
    color: #000; font-weight: 800; border-radius: 8px; height: 45px;
}
.signal-card {
    background: rgba(22,27,34,0.95);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    border-left: 5px solid #00ff88;
}
.live-signal { border-left-color: #00ff88; }
.sim-signal { border-left-color: #ffaa00; }
.agg-box {
    background: rgba(28,33,40,0.8);
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #30363d;
}
</style>
""", unsafe_allow_html=True)

# ================= CONSTANTS =================
XTB_PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "XAU/USD", "USOIL", "EUR/GBP", "NZD/USD"]

# ================= HELPERS =================
def parse_date(signal):
    try:
        return datetime.strptime(signal["full_date"], "%Y-%m-%d %H:%M:%S")
    except:
        return datetime.min

def calculate_rsi_adjusted(rsi_base, tf):
    shifts = {"1m": -25, "5m": -20, "15m": -15, "30m": -10, "1h": -5, "4h": 0, "1D": 5}
    return max(10, min(90, rsi_base + shifts.get(tf, 0)))

# ================= DATA =================
@st.cache_data(ttl=900)
def load_live_signals():
    signals = [
        {
            "pair": "EURUSD",
            "sym": "FX:EURUSD",
            "full_date": "2026-01-14 22:00:00",
            "type": "SPRZEDAŻ",
            "in": "1.16825",
            "sl": "1.18056",
            "tp": "1.16210",
            "src": "BESTFREESIGNAL",
            "url": "https://www.bestfreesignal.com",
            "live": True,
            "score": 92
        },
        {
            "pair": "XAUUSD",
            "sym": "OANDA:XAUUSD",
            "full_date": "2026-01-15 00:45:00",
            "type": "KUPNO",
            "in": "4615.90",
            "sl": "4402.70",
            "tp": "4722.50",
            "src": "BESTFREESIGNAL",
            "url": "https://www.bestfreesignal.com",
            "live": True,
            "score": 95
        }
    ]

    for s in signals:
        s.update({
            "inv": s["type"],
            "tv": s["type"],
            "rsi_base": random.randint(40, 60),
            "ma20": s["type"],
            "ma50": s["type"]
        })

    return signals

def generate_simulated_signals(n=5):
    signals = []
    prices = {
        "GBP/USD": 1.2750,
        "USD/JPY": 145.20,
        "AUD/USD": 0.6750,
        "USD/CAD": 1.3450,
        "USOIL": 72.50
    }

    for i, pair in enumerate(XTB_PAIRS[:n]):
        now = datetime.now() - timedelta(hours=i)
        base = prices.get(pair, 1.1000)
        t = random.choice(["KUPNO", "SPRZEDAŻ"])

        if t == "KUPNO":
            sl = base - 0.01
            tp = base + 0.03
        else:
            sl = base + 0.01
            tp = base - 0.03

        signals.append({
            "pair": pair,
            "sym": "FX:" + pair.replace("/", ""),
            "full_date": now.strftime("%Y-%m-%d %H:%M:%S"),
            "type": t,
            "in": f"{base:.4f}",
            "sl": f"{sl:.4f}",
            "tp": f"{tp:.4f}",
            "src": "XTB AI",
            "url": "https://www.xtb.com",
            "live": False,
            "score": random.randint(80, 94),
            "inv": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "tv": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "rsi_base": random.randint(35, 65),
            "ma20": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "ma50": random.choice(["KUPNO", "SPRZEDAŻ"])
        })

    return signals

# ================= SESSION =================
if "signals" not in st.session_state:
    st.session_state.signals = load_live_signals() + generate_simulated_signals()

if "active_signal" not in st.session_state:
    st.session_state.active_signal = st.session_state.signals[0]

if "view" not in st.session_state:
    st.session_state.view = "terminal"

# ================= UI =================
def render_signal_card(signal):
    cls = "live-signal" if signal["live"] else "sim-signal"
    color = "#00ff88" if signal["type"] == "KUPNO" else "#ff4b4b"

    st.markdown(f"""
    <div class="signal-card {cls}">
        <h4 style="color:{color}">{signal['pair']} | {signal['type']}</h4>
        <div>{signal['full_date']}</div>
        <div>IN {signal['in']} | SL {signal['sl']} | TP {signal['tp']}</div>
        <div>{signal['src']} | SCORE {signal['score']}%</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📊 ANALIZA", key=f"{signal['pair']}_{signal['full_date']}"):
        st.session_state.active_signal = signal
        st.rerun()

def render_detail(signal):
    st.subheader(f"{signal['pair']} | {signal['type']} | {signal['score']}%")

    tf = st.select_slider("RSI TF", ["1m", "5m", "15m", "30m", "1h", "4h", "1D"], "1D")
    rsi = calculate_rsi_adjusted(signal["rsi_base"], tf)

    st.markdown(f"<div class='agg-box'>RSI {tf}: <b>{rsi}</b></div>", unsafe_allow_html=True)

    components.html(f"""
    <script src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js"></script>
    <div class="tradingview-widget-container">
    <script>
    new TradingView.widget({{
        "symbol": "{signal.get('sym','FX:EURUSD')}",
        "interval": "D",
        "theme": "dark",
        "style": "1",
        "width": "100%",
        "height": 400
    }});
    </script>
    </div>
    """, height=420)

# ================= MAIN =================
st.title("🚀 TERMINAL V6.1 | LIVE + AI")

col1, col2 = st.columns([2, 3])

with col1:
    for s in sorted(st.session_state.signals, key=parse_date, reverse=True):
        render_signal_card(s)

with col2:
    render_detail(st.session_state.active_signal)
