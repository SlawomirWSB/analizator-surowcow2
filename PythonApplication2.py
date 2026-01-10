import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja interfejsu
st.set_page_config(layout="wide", page_title="XTB HUB V79", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #3d4451;
    }
    .data-box {
        background: rgba(0,0,0,0.4);
        padding: 8px;
        border-radius: 5px;
        margin: 5px 0;
        font-family: 'Courier New', monospace;
    }
    .verify-badge {
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        background: #161a25;
        border: 1px solid #2a2e39;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Dane (zgodne z obraz.png V63)
DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "upd": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "sym": "FX:GBPCHF", "inv": "STRONG SELL", "tv": "SELL"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "upd": "12:30", "type": "KUPNO", "color": "#00ff88", "sym": "FX:GBPAUD", "inv": "BUY", "tv": "STRONG BUY"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "upd": "06:47", "type": "KUPNO", "color": "#00ff88", "sym": "FX:CADJPY", "inv": "STRONG BUY", "tv": "BUY"}
}

def main():
    st.title("Terminal V79 - Full Data Restore")
    
    # Globalny wybór interwału (obraz.png V68)
    tf_val = st.select_slider("Wybierz interwał analizy:", options=["1h", "4h", "1d"], value="1d")
    
    if 'active_pair' not in st.session_state: st.session_state.active_pair = "GBP/CHF"
    
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        st.subheader("📩 Aktywne Sygnały")
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span>{pair}</span> <span style="color:{d['color']}">{d['type']}</span>
                    </div>
                    <div class="data-box">
                        IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}
                    </div>
                    <small style="color:#63676a;">🕒 Aktualizacja: {d['upd']} | TF: {tf_val}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Analizuj {pair}", key=pair):
                st.session_state.active_pair = pair
            st.link_button(f"✈️ Otwórz oryginał {pair}", "https://t.me/s/signalsproviderfx")

    with col_right:
        p = st.session_state.active_pair
        st.subheader(f"📊 Weryfikacja: {p} ({tf_val})")
        
        # Dwa źródła tekstowe (obraz.png V63/V65)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="verify-badge"><small>Investing.com</small><br><b style="color:{DB[p]["color"]}">{DB[p]["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="verify-badge"><small>TradingView Text</small><br><b style="color:{DB[p]["color"]}">{DB[p]["tv"]}</b></div>', unsafe_allow_html=True)
            
        st.write("---")
        
        # WIDGET - Uproszczona wersja skryptu (obraz.png zegary)
        tv_html = f"""
        <div style="height:450px;">
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
        {{
          "interval": "{tf_val}",
          "width": "100%",
          "isTransparent": true,
          "height": 450,
          "symbol": "{DB[p]['sym']}",
          "showIntervalTabs": false,
          "displayMode": "multiple",
          "locale": "pl",
          "colorTheme": "dark"
        }}
        </script>
        </div>
        """
        components.html(tv_html, height=480)

if __name__ == "__main__":
    main()
