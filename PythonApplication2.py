import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja V93 - Multi-Source & Sync
st.set_page_config(layout="wide", page_title="HUB V93")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .mobile-header { font-size: 0.9rem; font-weight: bold; color: #63676a; margin-top: -30px; margin-bottom: 15px; }
    
    /* Naprawa widoczności przycisków */
    div.stButton > button {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4b4d5a !important;
        font-weight: bold !important;
    }
    
    .signal-card {
        background-color: #1e222d; border-radius: 8px; padding: 12px;
        margin-bottom: 10px; border-left: 5px solid #3d4451;
    }
    
    .upd-time { font-size: 0.7rem; color: #888; text-align: right; }
    
    .data-row {
        background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0;
        font-family: monospace; color: #00ff88; font-weight: bold;
        text-align: center; border: 1px solid #333; font-size: 0.95rem;
    }
    
    .stat-box {
        background-color: #161a25; border: 1px solid #2a2e39;
        border-radius: 8px; padding: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych z dedykowanymi linkami
DB = {
    "GBP/CHF": {
        "in": "1.073", "tp": "1.071", "sl": "1.075", "sym": "FX:GBPCHF", "type": "SPRZEDAŻ", "color": "#ff4b4b", "upd": "10.01.2026 | 12:20",
        "tg": "https://t.me/s/signalsproviderfx",
        "rsi": {"1m": "38.2", "5m": "44.5", "1h": "52.1", "1D": "48.9"}
    },
    "GBP/AUD": {
        "in": "2.003", "tp": "2.007", "sl": "1.998", "sym": "FX:GBPAUD", "type": "KUPNO", "color": "#00ff88", "upd": "10.01.2026 | 12:30",
        "tg": "https://t.me/s/signalsproviderfx",
        "rsi": {"1m": "41.5", "5m": "54.8", "1h": "58.2", "1D": "61.3"}
    },
    "CAD/JPY": {
        "in": "113.85", "tp": "114.50", "sl": "113.30", "sym": "FX:CADJPY", "type": "KUPNO", "color": "#00ff88", "upd": "10.01.2026 | 06:47",
        "tg": "https://t.me/s/prosignalsfxx",
        "rsi": {"1m": "45.9", "5m": "51.2", "1h": "59.8", "1D": "62.4"}
    }
}

def main():
    st.markdown('<div class="mobile-header">V93 - MULTI-TG SOURCE</div>', unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    
    col_l, col_r = st.columns([1, 1.8])
    
    with col_l:
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between;">
                        <div><b style="font-size:1.1rem;">{pair}</b><br>
                        <span style="color:{d['color']}; font-weight:bold; font-size:0.9rem;">{d['type']}</span></div>
                        <div class="upd-time">🕒 {d['upd']}</div>
                    </div>
                    <div class="data-row">IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"📊 ANALIZA", key=f"btn_an_{pair}", use_container_width=True):
                    st.session_state.active = pair
            with c2:
                # Dynamiczny link Telegram zależny od instrumentu
                st.link_button(f"✈️ TELEGRAM", d['tg'], use_container_width=True)

    with col_r:
        sel = st.session_state.active
        selected_tf = st.select_slider("Interwał analizy:", 
                                     options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
        
        current_rsi = DB[sel]["rsi"].get(selected_tf, "50.0")
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="stat-box"><small>Investing ({selected_tf})</small><br><b style="color:{DB[sel]["color"]}">{DB[sel]["type"]}</b></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-box"><small>TradingView ({selected_tf})</small><br><b style="color:{DB[sel]["color"]}">{DB[sel]["type"]}</b></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {sel}</small><br><b style="color:#3498db;">{current_rsi}</b></div>', unsafe_allow_html=True)

        gauge_html = f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{selected_tf}", "width": "100%", "isTransparent": true, "height": 400,
            "symbol": "{DB[sel]['sym']}", "showIntervalTabs": false, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>
        """
        components.html(gauge_html, height=420)

if __name__ == "__main__": main()
