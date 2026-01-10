import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V39 - SENTIMENT", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 8px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Instrumentów (Uzupełniona o ID sentymentu)
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "OANDA:XAUUSD", "inv": "8830", "dfx": "gold"},
        "SILVER (Srebro)": {"tv": "OANDA:XAGUSD", "inv": "8836", "dfx": "silver"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "inv": "8849", "dfx": "us-crunch-oil"},
        "NATGAS (Gaz)": {"tv": "TVC:NATGAS", "inv": "8862", "dfx": "natural-gas"},
        "COCOA (Kakao)": {"tv": "ICEUS:CC1!", "inv": "8894", "dfx": ""},
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "NASDAQ:NDX", "inv": "14958", "dfx": "nasdaq-100"},
        "US500 (S&P500)": {"tv": "TVC:SPX", "inv": "166", "dfx": "sp-500"},
        "DE30 (DAX)": {"tv": "GLOBALPRIME:GER30", "inv": "172", "dfx": "germany-30"},
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "inv": "1", "dfx": "eur-usd"},
        "USDPLN": {"tv": "OANDA:USDPLN", "inv": "40", "dfx": ""},
        "GBPUSD": {"tv": "FX:GBPUSD", "inv": "2", "dfx": "gbp-usd"},
    }
}

def main():
    with st.sidebar:
        st.title("💰 XTB TERMINAL")
        st.info("### SENTYMENT RYNKU\nJeśli >70% kupuje, uważaj na odwrócenie trendu!")
        st.markdown("---")
        st.caption("V39 | Sentiment & Technicals")

    # PANEL WYBORU
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)
    with c4: audio = st.checkbox("Dźwięk", value=True)

    tv_symbol = DB[rynek][inst]["tv"]
    inv_id = DB[rynek][inst]["inv"]
    dfx_id = DB[rynek][inst]["dfx"]
    tv_interval = f"{itv}" if itv != "D" else "1D"

    st.subheader(f"🛡️ Triple Verification System: {inst}")
    
    # TRZY KOLUMNY: Sentyment | Sygnał | Detale
    col_sent, col_inv, col_tv = st.columns([1, 1, 2])

    with col_sent:
        st.markdown("<p style='font-size:11px; color:#83888D; text-align:center;'>SENTYMENT (DAILYFX)</p>", unsafe_allow_html=True)
        if dfx_id:
            # Widżet sentymentu od DailyFX/IG
            sent_url = f"https://www.dailyfx.com/sentiment-widget/{dfx_id}"
            components.html(f'<iframe src="{sent_url}" width="100%" height="450" frameborder="0"></iframe>', height=460)
        else:
            st.warning("Sentyment niedostępny dla tego aktywa")

    with col_inv:
        st.markdown("<p style='font-size:11px; color:#83888D; text-align:center;'>SYGNAŁ (INVESTING)</p>", unsafe_allow_html=True)
        tech_inv = f"""
        <iframe src="https://ssltsw.investing.com?lang=51&forex={inv_id}&commodities={inv_id}&indices={inv_id}&stocks=&equities=&single_stock={inv_id}&indices_id={inv_id}&quotes_id={inv_id}&stocks_id=&time_frame=900" 
        width="100%" height="450" frameborder="0"></iframe>
        """
        components.html(tech_inv, height=460)

    with col_tv:
        st.markdown("<p style='font-size:11px; color:#83888D; text-align:center;'>ANALIZA (TRADINGVIEW)</p>", unsafe_allow_html=True)
        tech_tv = f"""
        <div style="height: 450px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
          "interval": "{tv_interval if tv_interval == '1D' else tv_interval+'m'}",
          "width": "100%", "height": 450, "isTransparent": true, "symbol": "{tv_symbol}",
          "showIntervalTabs": true, "displayMode": "multiple", "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>
        """
        components.html(tech_tv, height=460)

    # WYKRES GŁÓWNY
    st.markdown("---")
    components.html(f"""
        <div id="tv_chart_main" style="height: 500px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "width": "100%", "height": 500, "symbol": "{tv_symbol}", "interval": "{itv}",
          "theme": "dark", "style": "1", "locale": "pl", "container_id": "tv_chart_main"
        }});
        </script>
    """, height=520)

if __name__ == "__main__":
    main()
