import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony - Tryb szeroki
st.set_page_config(layout="wide", page_title="XTB PRO TERMINAL V41", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja tła i ramek
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 12px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. INTELIGENTNA BAZA INSTRUMENTÓW
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "OANDA:XAUUSD", "inv": "8830"},
        "SILVER (Srebro)": {"tv": "OANDA:XAGUSD", "inv": "8836"},
        "COCOA (Kakao)": {"tv": "ICEUS:CC1!", "inv": "8894"},
        "COFFEE (Kawa)": {"tv": "ICEUS:KC1!", "inv": "8832"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "inv": "8849"},
        "NATGAS (Gaz)": {"tv": "TVC:NATGAS", "inv": "8862"}
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "NASDAQ:NDX", "inv": "14958"},
        "US500 (S&P500)": {"tv": "TVC:SPX", "inv": "166"},
        "DE30 (DAX)": {"tv": "GLOBALPRIME:GER30", "inv": "172"},
        "WIG20 (Polska)": {"tv": "GPW:WIG20", "inv": "10668"}
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "inv": "1"},
        "USDPLN": {"tv": "OANDA:USDPLN", "inv": "40"},
        "GBPUSD": {"tv": "FX:GBPUSD", "inv": "2"}
    }
}

def main():
    # MENU WYBORU
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Wybierz rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)
    with c4: audio = st.checkbox("Alert Audio", value=True)

    selected = DB[rynek][inst]
    tv_interval = f"{itv}" if itv != "D" else "1D"

    st.subheader(f"🛡️ Triple-Check Terminal: {inst}")

    # --- PANEL ANALIZY (3 KOLUMNY) ---
    col_1, col_2, col_3 = st.columns([1, 1, 1])

    with col_1:
        st.caption("📶 SYGNAŁ 1: SENTYMENT (Cena vs Tłum)")
        # Nowy, stabilny widżet sentymentu/techniczny
        components.html(f"""
            <div style="height: 450px;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{
              "interval": "{tv_interval}", "width": "100%", "height": 450,
              "isTransparent": true, "symbol": "{selected['tv']}", "showIntervalTabs": false,
              "displayMode": "single", "locale": "pl", "colorTheme": "dark"
            }}
            </script></div>
        """, height=460)

    with col_2:
        st.caption("⚖️ SYGNAŁ 2: WERDYKT (Investing)")
        # Investing - stabilne źródło zewnętrzne
        inv_url = f"https://ssltsw.investing.com?lang=51&forex={selected['inv']}&commodities={selected['inv']}&indices={selected['inv']}&stocks=&time_frame=900"
        components.html(f'<iframe src="{inv_url}" width="100%" height="450" frameborder="0"></iframe>', height=460)

    with col_3:
        st.caption("⏱️ SYGNAŁ 3: ZEGARY (TradingView)")
        # Klasyczne zegary oscylatorów
        components.html(f"""
            <div style="height: 450px;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{
              "interval": "{tv_interval}", "width": "100%", "height": 450,
              "isTransparent": true, "symbol": "{selected['tv']}", "showIntervalTabs": true,
              "displayMode": "multiple", "locale": "pl", "colorTheme": "dark"
            }}
            </script></div>
        """, height=460)

    # --- WYKRES DOLNY (ŚWIECZKI) ---
    st.markdown("---")
    components.html(f"""
        <div id="main_chart" style="height: 600px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "width": "100%", "height": 600, "symbol": "{selected['tv']}", "interval": "{itv}",
          "theme": "dark", "style": "1", "locale": "pl", "container_id": "main_chart",
          "withdateranges": true, "hide_side_toolbar": false, "allow_symbol_change": true
        }});
        </script>
    """, height=620)

if __name__ == "__main__":
    main()
