import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB ULTIMATE TERMINAL V40", page_icon="🚀")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja CSS dla profesjonalnego wyglądu
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 10px; background: #131722; border: 1px solid #2a2e39; }
    .stSelectbox label { color: #83888D !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. KOMPLETNA BAZA INSTRUMENTÓW XTB
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "OANDA:XAUUSD", "inv": "8830", "sent": "XAU/USD"},
        "SILVER (Srebro)": {"tv": "OANDA:XAGUSD", "inv": "8836", "sent": "XAG/USD"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "inv": "8849", "sent": "WTI"},
        "NATGAS (Gaz)": {"tv": "TVC:NATGAS", "inv": "8862", "sent": "NATGAS"},
        "COCOA (Kakao)": {"tv": "ICEUS:CC1!", "inv": "8894", "sent": "COCOA"},
        "COFFEE (Kawa)": {"tv": "ICEUS:KC1!", "inv": "8832", "sent": "COFFEE"},
        "COPPER (Miedź)": {"tv": "COMEX:HG1!", "inv": "8831", "sent": "COPPER"},
        "PLATINUM (Platyna)": {"tv": "NYMEX:PL1!", "inv": "8831", "sent": "PLATINUM"},
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "NASDAQ:NDX", "inv": "14958", "sent": "NAS100"},
        "US500 (S&P500)": {"tv": "TVC:SPX", "inv": "166", "sent": "SPX500"},
        "DE30 (DAX)": {"tv": "GLOBALPRIME:GER30", "inv": "172", "sent": "GER30"},
        "WIG20 (Polska)": {"tv": "GPW:WIG20", "inv": "10668", "sent": "WIG20"},
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "inv": "1", "sent": "EUR/USD"},
        "USDPLN": {"tv": "OANDA:USDPLN", "inv": "40", "sent": "USD/PLN"},
        "GBPUSD": {"tv": "FX:GBPUSD", "inv": "2", "sent": "GBP/USD"},
    }
}

def main():
    # --- PANEL STEROWANIA ---
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)
    with c4: audio = st.checkbox("Alert Audio", value=True)

    selected = DB[rynek][inst]
    tv_interval = f"{itv}" if itv != "D" else "1D"

    st.subheader(f"🛡️ Triple Verification: {inst}")
    
    # --- TRZY FILARY ANALIZY ---
    col_1, col_2, col_3 = st.columns([1, 1, 1.8])

    with col_1:
        st.markdown("<p style='font-size:11px; color:#5DADE2; text-align:center;'>1. SENTYMENT (Dfx/IG)</p>", unsafe_allow_html=True)
        # Sentyment rynkowy - czystsza wersja
        sent_url = f"https://it.tradingeconomics.com/embed/?s={selected['sent']}&h=450"
        components.html(f'<iframe src="{sent_url}" width="100%" height="450" frameborder="0"></iframe>', height=460)

    with col_2:
        st.markdown("<p style='font-size:11px; color:#FF4B4B; text-align:center;'>2. WERDYKT (Investing)</p>", unsafe_allow_html=True)
        # Techniczny sygnał Investing
        inv_url = f"https://ssltsw.investing.com?lang=51&forex={selected['inv']}&commodities={selected['inv']}&indices={selected['inv']}&stocks=&time_frame=900"
        components.html(f'<iframe src="{inv_url}" width="100%" height="450" frameborder="0"></iframe>', height=460)

    with col_3:
        st.markdown("<p style='font-size:11px; color:#00FFA2; text-align:center;'>3. DETALE (TradingView)</p>", unsafe_allow_html=True)
        # Zegary TradingView
        tv_widget = f"""
        <div style="height: 450px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
          "interval": "{tv_interval if tv_interval == '1D' else tv_interval+'m'}",
          "width": "100%", "height": 450, "isTransparent": true, "symbol": "{selected['tv']}",
          "showIntervalTabs": true, "displayMode": "multiple", "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>
        """
        components.html(tv_widget, height=460)

    # --- WYKRES INTERAKTYWNY ---
    st.markdown("---")
    components.html(f"""
        <div id="tv_chart_container" style="height: 550px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "width": "100%", "height": 550, "symbol": "{selected['tv']}", "interval": "{itv}",
          "theme": "dark", "style": "1", "locale": "pl", "container_id": "tv_chart_container",
          "hide_side_toolbar": false, "allow_symbol_change": true, "details": true
        }});
        </script>
    """, height=570)

    if audio:
        audio_script = """<script>setInterval(() => {if (document.body.innerText.includes('Mocne Kupno')) {new AudioContext().resume();}}, 60000);</script>"""
        components.html(audio_script, height=0)

if __name__ == "__main__":
    main()
