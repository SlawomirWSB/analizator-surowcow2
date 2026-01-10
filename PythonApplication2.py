import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja V87 - Mobile First Optimization
st.set_page_config(layout="wide", page_title="HUB V87")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Zmniejszony nagłówek dla telefonów */
    .mobile-header {
        font-size: 1.2rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        color: #63676a;
    }
    
    /* Naprawa odstępów Streamlit */
    .block-container { padding-top: 1rem !important; }

    /* Przyciski obok siebie - V86 Fix */
    div.stButton > button {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4b4d5a !important;
        font-weight: bold !important;
        height: 40px;
        font-size: 0.9rem;
    }
    
    .stLinkButton > a {
        background-color: #1e222d !important;
        color: #00ff88 !important;
        border: 1px solid #00ff88 !important;
        font-weight: bold !important;
        height: 40px; display: flex; align-items: center; justify-content: center;
        text-decoration: none; border-radius: 4px; font-size: 0.9rem;
    }

    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
        border-left: 5px solid #3d4451;
    }

    .data-row {
        background: #000000;
        padding: 8px;
        border-radius: 5px;
        margin: 8px 0;
        font-family: monospace;
        color: #00ff88;
        font-weight: bold;
        text-align: center;
        border: 1px solid #333;
        font-size: 0.95rem;
    }

    .stat-box {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych - Poprawione etykiety
DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "sym": "FX:GBPCHF", "type": "SPRZEDAŻ", "color": "#ff4b4b", "rsi": "31.2"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "sym": "FX:GBPAUD", "type": "KUPNO", "color": "#00ff88", "rsi": "54.8"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "sym": "FX:CADJPY", "type": "KUPNO", "color": "#00ff88", "rsi": "61.3"}
}

def main():
    # Zmniejszony napis nagłówka
    st.markdown('<div class="mobile-header">Terminal V87 - Smart Sync</div>', unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    
    col_l, col_r = st.columns([1, 1.8])
    
    with col_l:
        for pair, d in DB.items():
            # Przywrócone KUPNO/SPRZEDAŻ zamiast LIVE
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.1rem;">{pair}</b>
                        <span style="background:{d['color']}; color:white; padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">{d['type']}</span>
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
        
        # Interwał sterujący wszystkim
        selected_tf = st.select_slider(
            "Interwał analizy:",
            options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"],
            value="1D"
        )
        
        # Rząd statystyk (Investing, TV, RSI)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-box"><small>Investing</small><br><b style="color:{DB[sel]["color"]}">{DB[sel]["type"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-box"><small>TradingView</small><br><b style="color:{DB[sel]["color"]}">{DB[sel]["type"]}</b></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14)</small><br><b style="color:#3498db;">{DB[sel]["rsi"]}</b></div>', unsafe_allow_html=True)
            
        # TRZY ZEGARY
        gauge_html = f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{selected_tf}",
            "width": "100%",
            "isTransparent": true,
            "height": 420,
            "symbol": "{DB[sel]['sym']}",
            "showIntervalTabs": false,
            "displayMode": "multiple",
            "locale": "pl",
            "colorTheme": "dark"
          }}
          </script>
        </div>
        """
        components.html(gauge_html, height=450)

if __name__ == "__main__": main()
