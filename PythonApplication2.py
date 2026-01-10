import streamlit as st
import streamlit.components.v1 as components

# 1. Stylizacja i konfiguracja
st.set_page_config(layout="wide", page_title="XTB HUB V81 - Dual Verify + Gauges", page_icon="⚙️")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski - wysoki kontrast */
    div.stButton > button {
        background-color: #2a2e39 !important;
        color: #ffffff !important;
        border: 1px solid #4b4d5a !important;
        font-weight: bold !important;
        width: 100%;
    }

    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 5px;
        border-left: 5px solid #3d4451;
    }

    .data-row {
        background: rgba(0,0,0,0.4);
        padding: 8px;
        border-radius: 5px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        color: #00ff88;
    }

    .agg-box {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        min-height: 80px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych (Pełne dane z V63/V64)
DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "upd": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "sym": "FX:GBPCHF", "inv": "STRONG SELL", "tv": "SELL"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "upd": "12:30", "type": "KUPNO", "color": "#00ff88", "sym": "FX:GBPAUD", "inv": "BUY", "tv": "STRONG BUY"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "upd": "06:47", "type": "KUPNO", "color": "#00ff88", "sym": "FX:CADJPY", "inv": "STRONG BUY", "tv": "BUY"}
}

def main():
    st.markdown("<h2 style='text-align:center;'>Terminal V81 - Dual Agregator + Gauges</h2>", unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1, 1.5])
    
    with col_l:
        st.subheader("📩 Sygnały")
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.1rem; font-weight:bold;">{pair}</span>
                        <span style="background:{d['color']}; color:white; padding:2px 8px; border-radius:4px; font-weight:bold; font-size:0.8rem;">{d['type']}</span>
                    </div>
                    <div class="data-row">IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}</div>
                    <small style="color:#63676a;">🕒 {d['upd']} | Interwał: 1D</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"WYBIERZ {pair}", key=f"btn_{pair}"):
                st.session_state.active = pair
            st.link_button(f"✈️ Telegram: {pair}", "https://t.me/s/signalsproviderfx")
            st.write("")

    with col_r:
        sel = st.session_state.active
        st.subheader(f"📊 Analiza: {sel}")
        
        # PRZYWRÓCONE DWA AGREGATY (Investing + TV Text)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="agg-box"><small>Investing.com</small><br><b style="color:{DB[sel]["color"]}; font-size:1.3rem;">{DB[sel]["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="agg-box"><small>TradingView Text</small><br><b style="color:{DB[sel]["color"]}; font-size:1.3rem;">{DB[sel]["tv"]}</b></div>', unsafe_allow_html=True)
            
        st.write("")
        
        # WIDGET TECHNICZNY (ZEGARY)
        gauge_widget_html = f"""
        <div class="tradingview-widget-container" style="width:100%; height:450px;">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{
              "interval": "1d",
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
        components.html(gauge_widget_html, height=480)
        st.caption("Podsumowanie techniczne: Oscylatory, Średnie kroczące i Werdykt.")

if __name__ == "__main__": main()
