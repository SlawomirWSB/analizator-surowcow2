import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylizacja
st.set_page_config(layout="wide", page_title="XTB HUB V73 - Native Widgets", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski weryfikacji */
    div.stButton > button {
        color: #ffffff !important;
        background-color: #2a2e39 !important;
        border: 1px solid #3d4451 !important;
        font-weight: bold !important;
        width: 100%;
    }
    
    /* Linki po lewej - Stylizacja */
    .stLinkButton > a {
        background-color: #1e222d !important;
        color: #3498db !important;
        border: 1px solid #3498db !important;
        font-size: 0.8rem !important;
        text-align: center;
    }

    .signal-card {
        background-color: #1e222d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 5px;
        border-left: 5px solid #3d4451;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych (10.01.2026)
DB = {
    "GBP/CHF": {"updated": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "symbol": "FX:GBPCHF", "link": "https://t.me/s/signalsproviderfx"},
    "GBP/AUD": {"updated": "12:30", "type": "KUPNO", "color": "#00ff88", "symbol": "FX:GBPAUD", "link": "https://t.me/s/signalsproviderfx"},
    "CAD/JPY": {"updated": "06:47", "type": "KUPNO", "color": "#00ff88", "symbol": "FX:CADJPY", "link": "https://t.me/s/prosignalsfxx"}
}

def main():
    st.markdown('<h2 style="text-align:center;">Terminal V73 - Native TV Widgets</h2>', unsafe_allow_html=True)

    # Globalny wybór interwału (Przekazywany do widgetu)
    interval_map = {"1H": "1h", "4H": "4h", "1D": "1d"}
    global_tf = st.select_slider("Interwał systemowy:", options=["1H", "4H", "1D"], value="1D")
    tv_interval = interval_map[global_tf]

    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1, 1.4])

    # --- PANEL LEWY: LISTA + LINKI ---
    with col_l:
        st.subheader("📩 Aktywne Sygnały")
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
            st.markdown("<br>", unsafe_allow_html=True)

    # --- PANEL PRAWY: ORYGINALNY WIDGET TRADINGVIEW ---
    with col_r:
        active_pair = DB[st.session_state.active]
        st.subheader(f"📊 Oryginalny Widget TV: {st.session_state.active} ({global_tf})")
        
        # Kod HTML oryginalnego widgetu TradingView
        tradingview_script = f"""
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
          "interval": "{tv_interval}",
          "width": "100%",
          "isTransparent": true,
          "height": "450",
          "symbol": "{active_pair['symbol']}",
          "showIntervalTabs": false,
          "displayMode": "multiple",
          "locale": "pl",
          "colorTheme": "dark"
        }}
          </script>
        </div>
        """
        
        # Renderowanie natywnego widgetu
        components.html(tradingview_script, height=500)
        
        st.info(f"Widget powyżej jest bezpośrednim podsumowaniem z TradingView dla interwału {global_tf}. Zawiera Oscylatory, Podsumowanie i Średnie Kroczące.")

if __name__ == "__main__": main()
