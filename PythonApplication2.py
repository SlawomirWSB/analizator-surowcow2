import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylizacja V85
st.set_page_config(layout="wide", page_title="XTB HUB V85 - Triple Gauge + RSI", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski obok siebie - V83/V84 Style */
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
        height: 38px; display: flex; align-items: center; justify-content: center;
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

    .rsi-box {
        background: #161a25;
        border: 1px solid #3498db;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Rozszerzona Baza Danych
DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "sym": "FX:GBPCHF", "inv": "STRONG SELL", "tv": "SELL", "rsi": "32.4 (Oversold)", "color": "#ff4b4b"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "sym": "FX:GBPAUD", "inv": "BUY", "tv": "STRONG BUY", "rsi": "64.2 (Bullish)", "color": "#00ff88"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "sym": "FX:CADJPY", "inv": "STRONG BUY", "tv": "BUY", "rsi": "58.7 (Neutral+)", "color": "#00ff88"}
}

def main():
    st.markdown("<h2 style='text-align:center;'>Terminal V85 - Triple Gauge + RSI Control</h2>", unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1, 1.6])
    
    with col_l:
        st.subheader("📩 Sygnały")
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.2rem;">{pair}</b>
                        <span style="background:{d['color']}; color:white; padding:2px 8px; border-radius:4px;">{d['inv']}</span>
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
        st.subheader(f"🔍 Pełna Analiza: {sel}")
        
        # Sekcja RSI i Agregatów
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div style="text-align:center; background:#161a25; padding:10px; border-radius:8px; border:1px solid #2a2e39;"><small>Investing</small><br><b style="color:{DB[sel]["color"]}">{DB[sel]["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="text-align:center; background:#161a25; padding:10px; border-radius:8px; border:1px solid #2a2e39;"><small>TradingView</small><br><b style="color:{DB[sel]["color"]}">{DB[sel]["tv"]}</b></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="rsi-box"><small>RSI (14)</small><br><b style="color:#3498db;">{DB[sel]["rsi"]}</b></div>', unsafe_allow_html=True)
            
        st.write("")
        
        # TRZY ZEGARY + WYBÓR INTERWAŁU
        # displayMode: multiple -> wymusza 3 zegary
        # showIntervalTabs: true -> przywraca 1m, 5m, 1h, 1d itd.
        gauge_html = f"""
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "1D",
            "width": "100%",
            "isTransparent": true,
            "height": 450,
            "symbol": "{DB[sel]['sym']}",
            "showIntervalTabs": true,
            "displayMode": "multiple",
            "locale": "pl",
            "colorTheme": "dark"
          }}
          </script>
        </div>
        """
        components.html(gauge_html, height=500)
        st.caption("Trzy filary analizy: Oscylatory, Podsumowanie i Średnie kroczące. Wybierz interwał powyżej zegarów.")

if __name__ == "__main__": main()
