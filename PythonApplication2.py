import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja V84
st.set_page_config(layout="wide", page_title="XTB HUB V84 - Gauge Final Fix", page_icon="🧭")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski obok siebie */
    div.stButton > button {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4b4d5a !important;
        font-weight: bold !important;
    }
    
    .stLinkButton > a {
        background-color: #1e222d !important;
        color: #00ff88 !important;
        border: 1px solid #00ff88 !important;
        font-weight: bold !important;
        text-align: center;
        display: flex; justify-content: center; align-items: center;
        text-decoration: none; border-radius: 4px; height: 38px;
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

    .agg-box {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych
DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "upd": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "tv_sym": "FX:GBPCHF", "inv": "STRONG SELL", "tv": "SELL"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "upd": "12:30", "type": "KUPNO", "color": "#00ff88", "tv_sym": "FX:GBPAUD", "inv": "BUY", "tv": "STRONG BUY"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "upd": "06:47", "type": "KUPNO", "color": "#00ff88", "tv_sym": "FX:CADJPY", "inv": "STRONG BUY", "tv": "BUY"}
}

def main():
    st.markdown("<h2 style='text-align:center;'>Terminal V84 - Gauge Control</h2>", unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1, 1.5])
    
    with col_l:
        st.subheader("📩 Aktywne Sygnały")
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.2rem;">{pair}</b>
                        <span style="background:{d['color']}; color:white; padding:2px 8px; border-radius:4px; font-weight:bold;">{d['type']}</span>
                    </div>
                    <div class="data-row">IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            c_b1, c_b2 = st.columns(2)
            with c_b1:
                if st.button(f"📊 ANALIZA", key=f"an_{pair}", use_container_width=True):
                    st.session_state.active = pair
            with c_b2:
                st.link_button(f"✈️ TELEGRAM", "https://t.me/s/signalsproviderfx", use_container_width=True)
            st.write("")

    with col_r:
        sel = st.session_state.active
        st.subheader(f"📈 Analiza Techniczna: {sel}")
        
        # Dual Agregat Tekstowy
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="agg-box"><small>Investing.com</small><br><b style="color:{DB[sel]["color"]}; font-size:1.4rem;">{DB[sel]["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="agg-box"><small>TradingView Text</small><br><b style="color:{DB[sel]["color"]}; font-size:1.4rem;">{DB[sel]["tv"]}</b></div>', unsafe_allow_html=True)
            
        st.write("")
        
        # POWRÓT DO ZEGARÓW (Gauge) - Wykorzystujemy najbardziej stabilny widget TradingView
        gauge_html = f"""
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "1D",
            "width": "100%",
            "isTransparent": true,
            "height": 450,
            "symbol": "{DB[sel]['tv_sym']}",
            "showIntervalTabs": false,
            "displayMode": "single",
            "locale": "pl",
            "colorTheme": "dark"
          }}
          </script>
        </div>
        """
        components.html(gauge_html, height=500)

if __name__ == "__main__": main()
