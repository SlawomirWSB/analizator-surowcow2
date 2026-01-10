import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja V80
st.set_page_config(layout="wide", page_title="XTB HUB V80", page_icon="🚀")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa czytelności przycisków */
    div.stButton > button {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4b4d5a !important;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        border-color: #00ff88 !important;
        color: #00ff88 !important;
    }

    .signal-card {
        background-color: #1e222d;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 8px;
        border-left: 5px solid #3d4451;
    }
    .data-row {
        background: rgba(0,0,0,0.5);
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        font-family: monospace;
        font-size: 1rem;
        color: #00ff88;
    }
    .badge {
        padding: 12px;
        border-radius: 8px;
        background: #161a25;
        border: 1px solid #2a2e39;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych (Synchronizacja 10.01.2026)
DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "upd": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "sym": "FX:GBPCHF", "inv": "STRONG SELL"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "upd": "12:30", "type": "KUPNO", "color": "#00ff88", "sym": "FX:GBPAUD", "inv": "BUY"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "upd": "06:47", "type": "KUPNO", "color": "#00ff88", "sym": "FX:CADJPY", "inv": "STRONG BUY"}
}

def main():
    st.markdown("<h2 style='text-align:center;'>Terminal V80 - Hybrid View</h2>", unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    
    col_l, col_r = st.columns([1, 1.6])
    
    with col_l:
        st.subheader("📩 Sygnały Live")
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.2rem;">{pair}</b>
                        <span style="background:{d['color']}; color:black; padding:2px 8px; border-radius:4px; font-weight:bold;">{d['type']}</span>
                    </div>
                    <div class="data-row">
                        IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}
                    </div>
                    <small style="color:#63676a;">🕒 Aktualizacja: {d['upd']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"WYBIERZ {pair}", key=f"btn_{pair}"):
                st.session_state.active = pair
            st.link_button(f"✈️ Telegram: {pair}", "https://t.me/s/signalsproviderfx")
            st.write("")

    with col_r:
        sel = st.session_state.active
        st.subheader(f"📊 Analiza: {sel}")
        
        # Panel weryfikacji (obraz.png V65)
        st.markdown(f"""
            <div class="badge">
                <small style="color:#b2b5be;">Investing.com Consensus</small><br>
                <b style="color:{DB[sel]['color']}; font-size:1.5rem;">{DB[sel]['inv']}</b>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # NOWY WIDGET: Mini Wykres z podglądem technicznym (bardziej odporny na blokady)
        mini_chart_html = f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
          {{
            "symbol": "{DB[sel]['sym']}",
            "width": "100%",
            "height": 400,
            "locale": "pl",
            "dateRange": "1D",
            "colorTheme": "dark",
            "isTransparent": true,
            "autosize": false,
            "largeChartUrl": ""
          }}
          </script>
        </div>
        """
        components.html(mini_chart_html, height=420)
        st.info("Jeśli powyżej nie widzisz wykresu, Twoja przeglądarka blokuje skrypty TradingView. Spróbuj wyłączyć AdBlocka.")

if __name__ == "__main__":
    main()
