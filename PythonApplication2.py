import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylizacja
st.set_page_config(layout="wide", page_title="XTB SIGNAL AGGREGATOR V50", page_icon="📡")

st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    .signal-card { 
        background-color: #1e222d; 
        padding: 10px; 
        border-radius: 10px; 
        border: 1px solid #2a2e39;
        margin-bottom: 20px;
    }
    iframe { border-radius: 8px; background: #f5f5f5; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Sygnałów
CHANNELS = {
    "SignalProvider": "signalsproviderfx",
    "TopTradingSignals": "top_tradingsignals",
    "VasilyTrader": "VasilyTrading",
    "ProSignalsFX": "prosignalsfxx"
}

def main():
    st.title("🎯 Agregator Sygnałów i Weryfikacja")
    
    # Przycisk instrukcji tłumaczenia
    st.info("💡 **WSKAZÓWKA**: Aby przetłumaczyć sygnały, kliknij prawym przyciskiem myszy wewnątrz okna sygnałów i wybierz 'Przetłumacz na język polski' (funkcja przeglądarki Chrome/Edge/Firefox).")

    # Layout: Lewa strona sygnały, Prawa strona weryfikacja
    col_signals, col_verify = st.columns([1.2, 1])

    with col_signals:
        st.subheader("📥 Najnowsze Sygnały (Live)")
        
        # Tworzymy zakładki dla każdego kanału
        tabs = st.tabs(list(CHANNELS.keys()))
        
        for tab, (name, handle) in zip(tabs, CHANNELS.items()):
            with tab:
                # Wyświetlamy widget podglądu kanału Telegram (Widget oficjalny)
                # To jest najbardziej odporna na blokady metoda
                tg_widget = f"""
                <script async src="https://telegram.org/js/telegram-widget.js?22" 
                data-telegram-discussion="{handle}" 
                data-tme-mode 
                data-width="100%"></script>
                
                <iframe src="https://tgstat.com/pl/channel/@{handle}/embed" 
                width="100%" height="600" frameborder="0"></iframe>
                """
                components.html(tg_widget, height=650)

    with col_verify:
        st.subheader("⚖️ Weryfikacja Techniczna")
        
        # Wybór instrumentu do weryfikacji
        inst = st.selectbox("Weryfikuj instrument:", ["GOLD", "EURUSD", "GBPUSD", "US100", "OIL", "COCOA"])
        
        # Mapowanie dla TradingView
        mapping = {"GOLD": "TVC:GOLD", "EURUSD": "FX:EURUSD", "GBPUSD": "FX:GBPUSD", "US100": "TVC:NDX", "OIL": "TVC:USOIL", "COCOA": "ICEUS:CC1!"}
        symbol = mapping[inst]
        
        # Widget z 3 zegarami
        tv_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%2215%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{symbol}%22%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        components.iframe(tv_url, height=480)
        
        st.markdown("---")
        # Mini wykres trendu
        chart_url = f"https://s.tradingview.com/widgetembed/?symbol={symbol}&interval=15&theme=dark&locale=pl"
        components.iframe(chart_url, height=400)

if __name__ == "__main__":
    main()
