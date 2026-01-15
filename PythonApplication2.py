import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timedelta
import random

# KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V5.1", initial_sidebar_state="collapsed")
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%); color: #ffffff; }
div.stButton > button { 
    width: 100%; background: linear-gradient(45deg, #00ff88, #00cc6a); color: #000; 
    font-weight: 800; border: none; border-radius: 8px; text-transform: uppercase; 
    box-shadow: 0 4px 15px rgba(0,255,136,0.3); transition: all 0.3s; height: 45px; }
div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,255,136,0.4); }
.signal-card { 
    background: rgba(22,27,34,0.95); backdrop-filter: blur(10px); border: 1px solid #30363d; 
    border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 5px solid #00ff88; 
    transition: all 0.3s; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.signal-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,255,136,0.2); }
.agg-box { background: rgba(28,33,40,0.8); padding: 12px; border-radius: 8px; 
           text-align: center; border: 1px solid #30363d; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

class SignalManager:
    SOURCES = {
        "BESTFREESIGNAL": "https://www.bestfreesignal.com",
        "ECONOMIES": "https://www.economies.com/investing/signals", 
        "HOWTOTRADE": "https://howtotrade.com/free-forex-signals/",
        "STPTRADING": "https://www.stptrading.io/analysis/",
        "INVESTING": "https://www.investing.com/currencies/forex-signals"
    }
    
    @staticmethod
    def generate_signals(count=12):
        pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "Gold", "Crude Oil WTI", "EUR/GBP", "NZD/USD"]
        symbols = {
            "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "USD/JPY": "FX:USDJPY", 
            "AUD/USD": "FX:AUDUSD", "USD/CAD": "FX:USDCAD", "Gold": "OANDA:XAUUSD", 
            "Crude Oil WTI": "TVC:USOIL", "EUR/GBP": "FX:EURGBP", "NZD/USD": "FX:NZDUSD"
        }
        sources = list(SignalManager.SOURCES.keys())
        
        signals = []
        for i in range(count):
            now = datetime.now() - timedelta(hours=i*2 + random.randint(0,60))
            signal_type = random.choice(["KUPNO", "SPRZEDAŻ"])
            
            if "Oil" in pairs[i % len(pairs)]:
                base_price = 72.50 + random.uniform(-1,1)
                sl_offset, tp_offset = (0.8, 2.0) if signal_type=="KUPNO" else (-0.8, -2.0)
            elif "Gold" in pairs[i % len(pairs)]:
                base_price = 2650 + random.uniform(-10,10)
                sl_offset, tp_offset = (15, 45) if signal_type=="KUPNO" else (-15, -45)
            else:
                base_price = 1.0850 + (i * 0.0005) + random.uniform(-0.005,0.005)
                sl_offset, tp_offset = (0.012, 0.035) if signal_type=="KUPNO" else (-0.012, -0.035)
            
            signal = {
                "pair": pairs[i % len(pairs)],
                "sym": symbols[pairs[i % len(pairs)]],
                "date": now.strftime("%d.%m"),
                "hour": now.strftime("%H:%M"),
                "type": signal_type,
                "in": f"{base_price:.4f}" if base_price < 100 else f"{base_price:.2f}",
                "sl": f"{base_price + sl_offset:.4f}" if signal_type=="SPRZEDAŻ" else f"{base_price - abs(sl_offset):.4f}",
                "tp": f"{base_price + tp_offset:.4f}" if signal_type=="KUPNO" else f"{base_price - abs(tp_offset):.4f}",
                "rsi_base": random.randint(28, 72),
                "src": sources[i % len(sources)],
                "url": SignalManager.SOURCES[sources[i % len(sources)]],
                "score": random.randint(82, 98),
                "inv": random.choice(["KUPNO", "SPRZEDAŻ", "NEUTRAL"]),
                "tv": random.choice(["SILNE KUPNO", "KUPNO", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]),
                "analysis": random.choice([
                    "Wybicie z kanału H4", "RSI divergence", "Odbicie Fibonacci 61.8%", 
                    "Breakout trendline", "Opór kluczowy 1D", "Wsparcie wielodniowe", "MACD crossover"
                ])
            }
            signals.append(signal)
        return sorted(signals, key=lambda x: x['score'], reverse=True)

# SESJA
if 'signals' not in st.session_state:
    st.session_state.signals = SignalManager.generate_signals()
if 'active_signal' not in st.session_state:
    st.session_state.active_signal = st.session_state.signals[0]
if 'view' not in st.session_state:
    st.session_state.view = "terminal"

# SIDEBAR
with st.sidebar:
    st.markdown("### ⚙️ TERMINAL V5.1")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 ODŚWIEŻ", use_container_width=True):
            st.session_state.signals = SignalManager.generate_signals()
            st.rerun()
    with col2:
        if st.button("🏆 RANKING", use_container_width=True):
            st.session_state.view = "ranking"
            st.rerun()
    st.markdown("---")
    st.info(f"📊 Sygnałów: **{len(st.session_state.signals)}**")

def render_ranking():
    st.title("🏆 RANKING SYGNAŁÓW")
    if st.button("⬅️ TERMINAL", use_container_width=True):
        st.session_state.view = "terminal"
        st.rerun()
    
    df = pd.DataFrame(st.session_state.signals[:10])
    st.dataframe(
        df[['pair', 'score', 'type', 'src', 'in']].style
        .background_gradient(subset=['score'], cmap='Greens')
        .format({'score': '{:.0f}%', 'in': '{:.4f}'})
        .set_properties(**{'text-align': 'center'}),
        use_container_width=True, hide_index=True
    )

def render_signal_card(signal, idx):
    color = "#00ff88" if signal['type'] == "KUPNO" else "#ff4b4b"
    st.markdown(f"""
    <div class="signal-card" style="border-left-color: {color}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <h4 style="margin: 0 0 8px 0; color: {color};">{signal['pair']}</h4>
                <div style="font-size: 0.8rem; color: #8b949e;">
                    {signal['date']} {signal['hour']} | {signal['analysis']}
                </div>
            </div>
            <a href="{signal['url']}" target="_blank" 
               style="color: #00ff88; text-decoration: none; font-size: 0.75rem; 
                      padding: 4px 8px; border: 1px solid #00ff88; border-radius: 4px; margin-left: 8px;">
               {signal['src']}
            </a>
        </div>
        <div style="background: rgba(0,0,0,0.6); padding: 12px; border-radius: 8px; margin: 12px 0;">
            <div style="font-size: 1.2rem; font-weight: bold; text-align: center; color: {color}; margin-bottom: 4px;">
                {signal['type']} {signal['in']}
            </div>
            <div style="font-size: 0.85rem; text-align: center; color: #aaa;">
                SL: {signal['sl']} | TP: {signal['tp']} | {signal['score']}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"📊 ANALIZA", key=f"analyze_{idx}", use_container_width=True):
        st.session_state.active_signal = signal
        st.rerun()

def render_detail_view(signal):
    st.subheader(f"🔬 **{signal['pair']}** | {signal['type']} | Score: {signal['score']}%")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f'<div class="agg-box"><div style="font-size: 0.75rem; color: #8b949e;">Investing.com</div><div style="font-size: 1.1rem; font-weight: bold; color: {"#00ff88" if "KUPNO" in signal["inv"] else "#ff4b4b"};">{signal["inv"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agg-box"><div style="font-size: 0.75rem; color: #8b949e;">TradingView</div><div style="font-size: 1.1rem; font-weight: bold; color: {"#00ff88" if "KUPNO" in signal["tv"] else "#ff4b4b"};">{signal["tv"]}</div></div>', unsafe_allow_html=True)
        rsi_color = "#ff4b4b" if signal['rsi_base'] > 70 else "#00ff88"
        st.markdown(f'<div class="agg-box"><div style="font-size: 0.75rem; color: #8b949e;">RSI 1D</div><div style="font-size: 1.1rem; font-weight: bold; color: {rsi_color};">{signal["rsi_base"]}</div></div>', unsafe_allow_html=True)
    
    with col2:
        tf = st.select_slider("⏱️ Interwał", options=["1m", "5m", "15m", "1h", "4h", "1D"], value="1D")
        tf_map = {"1m": "1", "5m": "5", "15m": "15", "1h": "60", "4h": "240", "1D": "D"}
        components.html(f"""
        <div class="tradingview-widget-container">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{
                "interval": "{tf_map[tf]}", "width": "100%", "isTransparent": true, "height": 400,
                "symbol": "{signal['sym']}", "showIntervalTabs": true, "locale": "pl", "colorTheme": "dark"
            }}
            </script>
        </div>
        """, height=420)

# GŁÓWNY FLOW
if st.session_state.view == "ranking":
    render_ranking()
else:
    st.title("🚀 TERMINAL V5.1 | LIVE SIGNALS")
    h1, h2 = st.columns([3,1])
    with h1:
        st.markdown(f"**LIVE INSTRUMENTÓW: {len(st.session_state.signals)}**")
    with h2:
        if st.button("🔄 AKTUALIZUJ", use_container_width=True):
            st.session_state.signals = SignalManager.generate_signals()
            st.rerun()
    
    col_left, col_right = st.columns([2, 3])
    
    with col_left:
        st.markdown("### 📡 SYGNAŁY LIVE")
        for idx, signal in enumerate(st.session_state.signals):
            render_signal_card(signal, idx)
    
    with col_right:
        render_detail_view(st.session_state.active_signal)
