import streamlit as st

# 1. Konfiguracja i Stylizacja
st.set_page_config(layout="wide", page_title="XTB HUB V78 - Final Gauge Fix", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Stylizacja kart sygnałów */
    .signal-card {
        background-color: #1e222d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 5px;
        border-left: 5px solid #3d4451;
    }

    .data-table {
        width: 100%;
        background: rgba(0,0,0,0.3);
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #2a2e39;
    }

    .aggregator-card {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        text-align: center;
    }

    /* Przyciski i Linki */
    div.stButton > button {
        background-color: #2a2e39 !important;
        color: white !important;
        width: 100%;
        border: 1px solid #3d4451 !important;
    }
    
    .stLinkButton > a {
        background-color: #1e222d !important;
        color: #3498db !important;
        border: 1px solid #3498db !important;
        display: block;
        text-align: center;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych (Synchronizacja 10.01.2026)
DB = {
    "GBP/CHF": {
        "updated": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "symbol": "FX:GBPCHF", 
        "in": "1.073", "tp": "1.071", "sl": "1.075", "link": "https://t.me/s/signalsproviderfx",
        "1D": {"inv": "STRONG SELL", "tv": "SELL"}
    },
    "GBP/AUD": {
        "updated": "12:30", "type": "KUPNO", "color": "#00ff88", "symbol": "FX:GBPAUD", 
        "in": "2.003", "tp": "2.007", "sl": "1.998", "link": "https://t.me/s/signalsproviderfx",
        "1D": {"inv": "BUY", "tv": "STRONG BUY"}
    },
    "CAD/JPY": {
        "updated": "06:47", "type": "KUPNO", "color": "#00ff88", "symbol": "FX:CADJPY", 
        "in": "113.85", "tp": "114.50", "sl": "113.30", "link": "https://t.me/s/prosignalsfxx",
        "1D": {"inv": "STRONG BUY", "tv": "BUY"}
    }
}

def main():
    st.markdown('<h2 style="text-align:center;">Terminal V78 - Triple Signal Verify</h2>', unsafe_allow_html=True)

    # Wybór interwału
    interval_map = {"1H": "1h", "4H": "4h", "1D": "1d"}
    global_tf = st.select_slider("Interwał weryfikacji:", options=["1H", "4H", "1D"], value="1D")
    tv_interval = interval_map[global_tf]

    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1.1, 1.4])

    # --- PANEL LEWY: LISTA SYGNAŁÓW (Pełne Dane) ---
    with col_l:
        st.subheader("📩 Sygnały Live")
        for pair, info in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {info['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.1rem; font-weight:bold;">{pair}</span>
                        <span style="background:{info['color']}; color:white; padding:2px 8px; border-radius:4px; font-weight:bold;">{info['type']}</span>
                    </div>
                    <div class="data-table">
                        <table style="width:100%; color:#b2b5be; font-size:0.85rem; text-align:left;">
                            <tr><th>IN</th><th>TP</th><th>SL</th></tr>
                            <tr style="color:white; font-weight:bold; font-size:1rem;">
                                <td>{info['in']}</td><td>{info['tp']}</td><td>{info['sl']}</td>
                            </tr>
                        </table>
                    </div>
                    <small style="color:#63676a;">🕒 Aktualizacja: {info['updated']} | TF: {global_tf}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Analiza {pair}", key=f"btn_{pair}"):
                st.session_state.active = pair
            st.link_button(f"✈️ Otwórz oryginał {pair}", info["link"], use_container_width=True)
            st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # --- PANEL PRAWY: AGREGATOR + WIDGET NATIVE ---
    with col_r:
        item = DB[st.session_state.active]
        data = item.get(global_tf, {"inv": "N/A", "tv": "N/A"})
        
        st.subheader(f"📊 {st.session_state.active} ({global_tf})")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="aggregator-card"><small>Investing.com</small><br><b style="color:{item["color"]}; font-size:1.4rem;">{data["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="aggregator-card"><small>TradingView Text</small><br><b style="color:{item["color"]}; font-size:1.4rem;">{data["tv"]}</b></div>', unsafe_allow_html=True)

        # OSTATECZNA METODA: Wymuszenie czystego HTML do body aplikacji
        # Widget z zegarami
        tv_widget_script = f"""
        <div class="tradingview-widget-container" style="width: 100%; height: 500px;">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{
              "interval": "{tv_interval}",
              "width": "100%",
              "isTransparent": true,
              "height": "100%",
              "symbol": "{item['symbol']}",
              "showIntervalTabs": false,
              "displayMode": "multiple",
              "locale": "pl",
              "colorTheme": "dark"
            }}
            </script>
        </div>
        """
        # Używamy st.components.v1.html z wyższym priorytetem ładowania
        st.components.v1.html(tv_widget_script, height=520, scrolling=False)
        st.caption(f"ℹ️ System analizuje 26 wskaźników technicznych dla {st.session_state.active}.")

if __name__ == "__main__": main()
