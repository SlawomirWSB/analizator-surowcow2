import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja V86 - Globalne Sterowanie Interwałem
st.set_page_config(layout="wide", page_title="XTB HUB V86 - Synchronized Analysis")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski w rzędzie pod sygnałem */
    div.stButton > button {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4b4d5a !important;
        font-weight: bold !important;
        height: 42px;
    }
    
    .stLinkButton > a {
        background-color: #1e222d !important;
        color: #00ff88 !important;
        border: 1px solid #00ff88 !important;
        font-weight: bold !important;
        height: 42px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; border-radius: 4px;
    }

    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #3d4451;
    }

    .data-row {
        background: #000000;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-family: monospace;
        color: #00ff88;
        font-weight: bold;
        text-align: center;
        border: 1px solid #333;
    }

    .stat-box {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych z dynamicznymi interwałami
# Mapowanie interwałów dla widgetu TV
TF_MAP = {
    "1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h", "1D": "1D", "1W": "1W"
}

DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "sym": "FX:GBPCHF", "color": "#ff4b4b"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "sym": "FX:GBPAUD", "color": "#00ff88"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "sym": "FX:CADJPY", "color": "#00ff88"}
}

def main():
    st.markdown("<h2 style='text-align:center;'>Terminal V86 - Synchronized Multi-Interval</h2>", unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    
    col_l, col_r = st.columns([1, 1.8])
    
    with col_l:
        st.subheader("📩 Sygnały Live")
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.2rem;">{pair}</b>
                        <span style="background:{d['color']}; color:white; padding:2px 8px; border-radius:4px;">LIVE</span>
                    </div>
                    <div class="data-row">IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"📊 ANALIZA", key=f"an_{pair}", use_container_width=True):
                    st.session_state.active = pair
            with c2:
                st.link_button(f"✈️ TELEGRAM", "https://t.me/s/signalsproviderfx", use_container_width=True)
            st.write("")

    with col_r:
        sel = st.session_state.active
        st.subheader(f"🔍 Pełna Weryfikacja: {sel}")
        
        # GLOBALNY WYBÓR INTERWAŁU (Zmienia wszystko poniżej)
        selected_tf = st.select_slider(
            "Ustaw interwał dla wszystkich wskaźników (Investing, TV, RSI, Zegary):",
            options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"],
            value="1D"
        )
        
        st.write("")
        
        # Rząd 1: Investing, TradingView, RSI (Synchronizowane)
        # W prawdziwym API te wartości zmieniałyby się zależnie od 'selected_tf'
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-box"><small>Investing ({selected_tf})</small><br><b>STRONG BUY</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-box"><small>TradingView ({selected_tf})</small><br><b>BUY</b></div>', unsafe_allow_html=True)
        with c3:
            # RSI zmienia się wizualnie dla demonstracji
            rsi_val = "62.5" if "1h" in selected_tf else "58.7"
            st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) - {selected_tf}</small><br><b style="color:#3498db;">{rsi_val} (Neutral+)</b></div>', unsafe_allow_html=True)
            
        st.write("")
        
        # TRZY ZEGARY (Gauge) - Synchronizowane interwałem
        # "showIntervalTabs": false (wyłączamy, bo mamy własny slider wyżej sterujący całością)
        gauge_html = f"""
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{selected_tf}",
            "width": "100%",
            "isTransparent": true,
            "height": 450,
            "symbol": "{DB[sel]['sym']}",
            "showIntervalTabs": false,
            "displayMode": "multiple",
            "locale": "pl",
            "colorTheme": "dark"
          }}
          </script>
        </div>
        """
        components.html(gauge_html, height=480)
        st.caption(f"Status: Dane zsynchronizowane dla interwału {selected_tf}.")

if __name__ == "__main__": main()
