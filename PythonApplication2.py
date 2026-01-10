import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB SIGNAL TERMINAL V55", page_icon="📈")

# 2. Stylizacja CSS
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3d4451;
        margin-bottom: 15px;
        color: white;
    }
    .buy { border-left-color: #00ff88; }
    .sell { border-left-color: #ff4b4b; }
    .price-txt { font-family: monospace; color: #8f94a1; font-size: 1.1rem; }
    .source-link { color: #37a6ef; text-decoration: none; font-size: 0.8rem; }
    iframe { border-radius: 10px; border: 1px solid #2a2e39 !important; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🎯 Terminal Sygnałowy: 10 Stycznia 2026")
    
    # GŁÓWNY UKŁAD: Lewa (Sygnały z Telegrama) | Prawa (Twoja Weryfikacja TV)
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("📥 Najnowsze Sygnały z Twoich Źródeł")
        
        # KARTA: CAD/JPY (ProSignalsFx)
        st.markdown(f"""
            <div class="signal-card buy">
                <div style="display: flex; justify-content: space-between;">
                    <b>📊 CAD/JPY - ProSignalsFx</b>
                    <span style="color: #00ff88;">🟢 LONG</span>
                </div>
                <div class="price-txt">Sygnał: Wybicie z formacji trójkąta</div>
                <div style="margin-top: 10px;">🎯 TP: Zielona strefa (wykres) | 🛡️ SL: Pod trójkątem</div>
                <div style="font-size: 0.85rem; margin: 10px 0;"><i>CAD/JPY jest nie do zatrzymania po kompresji ceny.</i></div>
                <a class="source-link" href="https://t.me/s/prosignalsfxx" target="_blank">🔗 Zobacz oryginalny wpis (Jan 10)</a>
            </div>
        """, unsafe_allow_html=True)

        # KARTA: GBP/CHF (SignalProvider)
        st.markdown(f"""
            <div class="signal-card sell">
                <div style="display: flex; justify-content: space-between;">
                    <b>📉 GBP/CHF - SignalProvider</b>
                    <span style="color: #ff4b4b;">🔴 SELL</span>
                </div>
                <div class="price-txt">Wejście: 1.073</div>
                <div style="margin-top: 10px;">🎯 TP: 1.071 | 🛡️ SL: 1.075</div>
                <div style="font-size: 0.85rem; margin: 10px 0;"><i>Rynek testuje główną strukturę horyzontalną. Spodziewany spadek.</i></div>
                <a class="source-link" href="https://t.me/s/signalsproviderfx" target="_blank">🔗 Zobacz oryginalny wpis (Jan 10)</a>
            </div>
        """, unsafe_allow_html=True)

        # KARTA: GOLD (VasilyTrader / Systemowy)
        st.markdown(f"""
            <div class="signal-card buy">
                <div style="display: flex; justify-content: space-between;">
                    <b>🥇 GOLD (Złoto) - VasilyTrader / TV</b>
                    <span style="color: #00ff88;">🟢 BUY</span>
                </div>
                <div class="price-txt">Cena rynkowa: 4509.66</div>
                <div style="margin-top: 10px;">🎯 TP: 4525.00 | 🛡️ SL: 4495.00</div>
                <div style="font-size: 0.85rem; margin: 10px 0;"><i>Odbicie od psychologicznego poziomu 4500. Zegary TV potwierdzają trend.</i></div>
                <a class="source-link" href="https://t.me/s/VasilyTrading" target="_blank">🔗 Zobacz analizę (Jan 10)</a>
            </div>
        """, unsafe_allow_html=True)

        st.info("💡 TopTradingSignals: Dzisiejsze wpisy to głównie analizy fundamentalne bez podanych parametrów wejścia.")

    with col_right:
        st.subheader("⚖️ Weryfikacja: GOLD (15m)")
        
        # Twoje ulubione zegary - Potwierdzenie techniczne
        # Ustawione na GOLD, interwał 15m (zgodnie z obraz.png)
        tv_url = "https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%2215%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22TVC:GOLD%22%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        components.iframe(tv_url, height=480)
        
        # Mały wykres pomocniczy na dole
        chart_url = "https://s.tradingview.com/widgetembed/?symbol=TVC:GOLD&interval=15&theme=dark&locale=pl"
        components.iframe(chart_url, height=350)

    st.markdown("---")
    st.caption("Pamiętaj: Darmowe sygnały z Telegrama zawsze weryfikuj z zegarami technicznymi przed wejściem w XTB.")

if __name__ == "__main__":
    main()
