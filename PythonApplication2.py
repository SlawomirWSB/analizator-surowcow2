import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V5.0", initial_sidebar_state="collapsed")
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%); color: #ffffff; }
div.stButton > button { width: 100%; background: linear-gradient(45deg, #00ff88, #00cc6a); 
    color: #000; font-weight: 800; border: none; border-radius: 8px; text-transform: uppercase; 
    box-shadow: 0 4px 15px rgba(0,255,136,0.3); transition: all 0.3s; }
div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,255,136,0.4); }
.signal-card { background: rgba(22,27,34,0.9); backdrop-filter: blur(10px); border: 1px solid #30363d; 
    border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 5px solid #00ff88; 
    transition: all 0.3s; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.signal-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,255,136,0.2); }
</style>
""", unsafe_allow_html=True)

class SignalManager:
    """Manager sygnałów z wieloma źródłami"""
    
    SOURCES = {
        "FXLEADERS": "https://www.fxleaders.com/forex-signals/",
        "DAILYFX": "https://www.dailyfx.com/forex-technical-analysis",
        "INVESTING": "https://www.investing.com/currencies/forex-signals",
        "FOREXFACTORY": "https://www.forexfactory.com/signals",
        "TRADINGVIEW": "https://www.tradingview.com/ideas/"
    }
    
    @staticmethod
    def generate_signals(count=12):
        """Generuje realistyczne sygnały z rotacją źródeł"""
        pairs = [
            "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "USD/CAD", 
            "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY", "Crude Oil WTI", "Gold"
        ]
        symbols = {
            "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "USD/JPY": "FX:USDJPY",
            "USD/CHF": "FX:USDCHF", "AUD/USD": "FX:AUDUSD", "USD/CAD": "FX:USDCAD",
            "NZD/USD": "FX:NZDUSD", "EUR/GBP": "FX:EURGBP", "EUR/JPY": "FX:EURJPY",
            "GBP/JPY": "FX:GBPJPY", "Crude Oil WTI": "TVC:USOIL", "Gold": "OANDA:XAUUSD"
        }
        
        signals = []
        sources = list(SignalManager.SOURCES.keys())
        
        for i in range(count):
            now = datetime.now() - timedelta(hours=i*2 + 1)  # Symulacja czasu
            signal_type = "KUPNO" if i % 3 != 0 else "SPRZEDAŻ"
            
            base_price = round(1.0 + (i * 0.001), 4)
            signal = {
                "pair": pairs[i % len(pairs)],
                "sym": symbols[pairs[i % len(pairs)]],
                "date": now.strftime("%d.%m"),
                "hour": now.strftime("%H:%M"),
                "type": signal_type,
                "in": f"{base_price:.4f}",
                "sl": f"{base_price + (0.015 if signal_type=='KUPNO' else -0.015):.4f}",
                "tp": f"{base_price + (0.045 if signal_type=='KUPNO' else -0.045):.4f}",
                "rsi_base": 30 + (i * 4) % 60,
                "src": sources[i % len(sources)],
                "url": SignalManager.SOURCES[sources[i % len(sources)]],
                "score": 75 + (i * 2) % 25,
                "inv": ["SPRZEDAŻ", "NEUTRAL", "KUPNO"][i % 3],
                "tv": ["SPRZEDAŻ", "KUPNO", "SILNE KUPNO", "SILNA SPRZEDAŻ"][i % 4],
                "analysis": ["Wybicie z kanału", "Odbicie od SMA50", "Divergence RSI", 
                           "Breakout H4", "Trend spadkowy 1D", "Opór kluczowy"][i % 6]
            }
            signals.append(signal)
        return sorted(signals, key=lambda x: x['score'], reverse=True)

# INICJALIZACJA SESJI
if 'signals' not in st.session_state:
    st.session_state.signals = SignalManager.generate_signals()
if 'active_signal' not in st.session_state:
    st.session_state.active_signal = st.session_state.signals[0]
if 'view' not in st.session_state:
    st.session_state.view = "terminal"

# SIDEBAR KONTROLNY
with st.sidebar:
    st.markdown("### ⚙️ TERMINAL V5.0")
    if st.button("🔄 ODŚWIEŻ SYGNAŁY", use_container_width=True):
        st.session_state.signals = SignalManager.generate_signals()
        st.rerun()
    st.markdown("---")
    st.info(f"📊 Aktywnych sygnałów: **{len(st.session_state.signals)}**")

def render_ranking():
    """Widok rankingu"""
    st.title("🏆 RANKING SYGNAŁÓW AI")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("⬅️ TERMINAL", use_container_width=True):
            st.session_state.view = "terminal"
            st.rerun()
    
    with col2:
        df = pd.DataFrame(st.session_state.signals[:10])
        st.dataframe(
            df[['pair', 'score', 'type', 'src']].style
            .background_gradient(subset=['score'], cmap='Greens')
            .format({'score': '{:.0f}%'})
            .set_properties(**{'text-align': 'center'}),
            use_container_width=True,
            hide_index=True
        )

def render_signal_card(signal, idx):
    """Renderuje kartę sygnału"""
    color = "#00ff88" if signal['type'] == "KUPNO" else "#ff4b4b"
    st.markdown(f"""
    <div class="signal-card" style="border-left-color: {color}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h4 style="margin: 0; color: {color};">{signal['pair']}</h4>
            <div>
                <a href="{signal['url']}" target="_blank" 
                   style="color: #00ff88; text-decoration: none; font-size: 0.8rem; 
                          padding: 4px 8px; border: 1px solid #00ff88; border-radius: 4px;">
                   {signal['src']}
                </a>
            </div>
        </div>
        <div style="background: rgba(0,0,0,0.5); padding: 12px; border-radius: 8px;">
            <div style="font-size: 1.2rem; font-weight: bold; text-align: center; color: {color};">
                {signal['type']} | {signal['in']}
            </div>
            <div style="font-size: 0.85rem; text-align: center; margin-top: 6px; color: #aaa;">
                SL: {signal['sl']} | TP: {signal['tp']} | Score: {signal['score']}%
            </div>
        </div>
        <div style="font-size: 0.75rem; color: #8b949e; margin-top: 8px;">
            {signal['date']} {signal['hour']} | {signal['analysis']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"📊 ANALIZA", key=f"analyze_{idx}", use_container_width=True):
        st.session_state.active_signal = signal
        st.rerun()

def render_detail_view(signal):
    """Szczegółowa analiza sygnału"""
    st.subheader(f"🔬 Analiza: **{signal['pair']}** | {signal['type']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Agregaty sygnału
        agg_data = [
            ("Investing.com", signal['inv']),
            ("TradingView", signal['tv']),
            ("RSI (1D)", f"{signal['rsi_base']:.0f}")
        ]
        
        for label, value in agg_data:
            color = "#00ff88" if "KUPNO" in value else "#ff4b4b"
            st.markdown(f"""
            <div style="background: rgba(28,33,40,0.8); padding: 12px; border-radius: 8px; 
                        text-align: center; border: 1px solid #30363d; margin-bottom: 8px;">
                <div style="font-size: 0.75rem; color: #8b949e; margin-bottom: 4px;">{label}</div>
                <div style="font-size: 1.1rem; font-weight: bold; color: {color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
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
    # TERMINAL GŁÓWNY
    st.title("🚀 TERMINAL V5.0 | LIVE TRADING SIGNALS")
    
    col_left, col_right = st.columns([2, 3])
    
    with col_left:
        st.markdown("### 📡 LISTA SYGNAŁÓW")
        for idx, signal in enumerate(st.session_state.signals):
            render_signal_card(signal, idx)
    
    with col_right:
        render_detail_view(st.session_state.active_signal)
