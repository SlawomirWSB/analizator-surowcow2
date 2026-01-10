import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylizacja
st.set_page_config(layout="wide", page_title="XTB HUB V74 - Triple Verify", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski operacyjne */
    div.stButton > button {
        color: #ffffff !important;
        background-color: #2a2e39 !important;
        border: 1px solid #3d4451 !important;
        font-weight: bold !important;
        width: 100%;
    }
    
    /* Linki pod każdą parą po lewej */
    .stLinkButton > a {
        background-color: #1e222d !important;
        color: #3498db !important;
        border: 1px solid #3498db !important;
        font-size: 0.8rem !important;
        padding: 8px !important;
        text-align: center;
        display: block;
        border-radius: 5px;
    }

    .signal-card {
        background-color: #1e222d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 5px;
        border-left: 5px solid #3d4451;
    }

    .aggregator-card {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych (Synchronizacja 10.01.2026)
DB = {
    "GBP/CHF": {
        "updated": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "symbol": "FX:GBPCHF", 
        "link": "https://t.me/s/signalsproviderfx",
        "1D": {"inv": "STRONG SELL", "tv": "SELL"},
        "4H": {"inv": "SELL", "tv": "NEUTRAL"},
        "1H": {"inv": "NEUTRAL", "tv": "BUY"}
    },
    "GBP/AUD": {
        "updated": "12:30", "type": "KUPNO", "color": "#00ff88", "symbol": "FX:GBPAUD", 
        "link": "https://t.me/s/signalsproviderfx",
        "1D": {"inv": "BUY", "tv": "STRONG BUY"},
        "4H": {"inv": "STRONG BUY", "tv": "STRONG BUY"},
        "1H": {"inv": "BUY", "tv": "BUY"}
    },
    "CAD/JPY": {
        "updated": "06:47", "type": "KUPNO", "color": "#00ff88", "symbol": "FX:CADJPY", 
        "link": "https://t.me/s/prosignalsfxx",
        "1D": {"inv": "STRONG BUY", "tv": "BUY"},
        "4H": {"inv": "BUY", "tv": "BUY"},
        "1H": {"inv": "NEUTRAL", "tv": "NEUTRAL"}
    }
}

def main():
    st.markdown('<h2 style="text-align:center;">Terminal V74 - Triple Verification System</h2>', unsafe_allow_html=True)

    # Globalny wybór interwału
    interval_map = {"1H": "1h", "4H": "4h", "1D": "1d"}
    global_tf = st.select_slider("Wybierz interwał analizy:", options=["1H", "4H", "1D"], value="1D")
    tv_interval = interval_map[global_tf]

    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1, 1.4])

    # --- PANEL LEWY: LISTA + LINKI ---
    with col_l:
        st.subheader("📩 Sygnały Live")
        for pair, info in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {info['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.2rem; font-weight:bold;">{pair}</span>
                        <span style="background:{info['color']}; color:white; padding:2px 10px; border-radius:5px; font-weight:bold;">{info['type']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Weryfikuj {pair}", key=f"v_{pair}"):
                st.session_state.active = pair
            st.link_button(f"✈️ Otwórz oryginał {pair}", info["link"], use_container_width=True)
            st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # --- PANEL PRAWY: DWA ŹRÓDŁA + WIDGET ---
    with col_r:
        item = DB[st.session_state.active]
        data = item[global_tf]
        
        st.subheader(f"📊 Pełna Weryfikacja {st.session_state.active} ({global_tf})")
        
        # Sekcja 1 & 2: Niezależne dane tekstowe
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="aggregator-card">
                <small style="color:#b2b5be;">Źródło: Investing.com</small><br>
                <b style="font-size:1.6rem; color:{item['color']}">{data['inv']}</b>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="aggregator-card">
                <small style="color:#b2b5be;">Źródło: TradingView Text</small><br>
                <b style="font-size:1.6rem; color:{item['color']}">{data['tv']}</b>
            </div>""", unsafe_allow_html=True)

        # Sekcja 3: Oryginalny Widget Graficzny
        st.markdown('<div style="background:#161a25; padding:10px; border-radius:10px; border:1px solid #2a2e39;">', unsafe_allow_html=True)
        tradingview_script = f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
          "interval": "{tv_interval}",
          "width": "100%",
          "isTransparent": true,
          "height": "420",
          "symbol": "{item['symbol']}",
          "showIntervalTabs": false,
          "displayMode": "multiple",
          "locale": "pl",
          "colorTheme": "dark"
        }}
          </script>
        </div>
        """
        components.html(tradingview_script, height=450)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.caption(f"ℹ️ Dane powyżej pochodzą z trzech niezależnych silników analitycznych dla interwału {global_tf}.")

if __name__ == "__main__": main()
