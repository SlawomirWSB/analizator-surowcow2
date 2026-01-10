import streamlit as st

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB SIGNAL HUB V56", page_icon="🎯")

# 2. Stylizacja CSS dla kart i agregatów
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
        cursor: pointer;
        transition: 0.3s;
    }
    .signal-card:hover { background-color: #2a2e39; border-left-width: 8px; }
    .buy { border-left-color: #00ff88 !important; }
    .sell { border-left-color: #ff4b4b !important; }
    .aggregator-box {
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 20px;
        min-height: 600px;
    }
    .status-tag { padding: 5px 10px; border-radius: 5px; font-weight: bold; }
    .tag-buy { background-color: rgba(0, 255, 136, 0.2); color: #00ff88; }
    .tag-sell { background-color: rgba(255, 75, 75, 0.2); color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza danych sygnałów i weryfikacji (Dane z 10 Stycznia 2026)
DATA = {
    "GBP/CHF": {
        "source": "SignalProvider",
        "type": "SELL",
        "price": "1.073",
        "tp": "1.071",
        "sl": "1.075",
        "note": "Rynek testuje opór horyzontalny. Spodziewany spadek.",
        "link": "https://t.me/s/signalsproviderfx/410",
        "investing": {"verdict": "SELL", "summary": "Indicators: Sell (5) / Buy (1)"},
        "tradingview": {"verdict": "NEUTRAL", "summary": "Moving Averages: Sell (7) / Buy (5)"}
    },
    "CAD/JPY": {
        "source": "ProSignalsFx",
        "type": "BUY",
        "price": "113.85",
        "tp": "114.50",
        "sl": "113.30",
        "note": "Wybicie z formacji trójkąta (kompresja). Silny pęd wzrostowy.",
        "link": "https://t.me/s/prosignalsfxx",
        "investing": {"verdict": "STRONG BUY", "summary": "Indicators: Buy (8) / Sell (0)"},
        "tradingview": {"verdict": "BUY", "summary": "Moving Averages: Buy (12) / Sell (2)"}
    },
    "GOLD": {
        "source": "VasilyTrader",
        "type": "BUY",
        "price": "4509.66",
        "tp": "4525.00",
        "sl": "4495.00",
        "note": "Odbicie od psychologicznego poziomu 4500.",
        "link": "https://t.me/s/VasilyTrading",
        "investing": {"verdict": "STRONG SELL", "summary": "Wskaźniki: Sell (5) / Buy (2)"},
        "tradingview": {"verdict": "STRONG BUY", "summary": "Średnie kroczące: Silne Kupno (13)"}
    }
}

def main():
    st.title("🎯 Terminal: Agregator Sygnałów (10.01.2026)")

    # Inicjalizacja stanu wyboru
    if 'selected_pair' not in st.session_state:
        st.session_state.selected_pair = "GOLD"

    col_feed, col_agg = st.columns([1, 1.2])

    # --- PANEL LEWY: LISTA SYGNAŁÓW ---
    with col_feed:
        st.subheader("📡 Sygnały Live (Kliknij, aby zweryfikować)")
        
        for pair, info in DATA.items():
            card_class = "buy" if info["type"] == "BUY" else "sell"
            if st.button(f"🔍 WERYFIKUJ: {pair} ({info['source']})", use_container_width=True):
                st.session_state.selected_pair = pair
            
            st.markdown(f"""
                <div class="signal-card {card_class}">
                    <b>{pair}</b> | {info['source']}<br>
                    <small>Kierunek: {info['type']} @ {info['price']}</small>
                </div>
            """, unsafe_allow_html=True)

    # --- PANEL PRAWY: AGREGATOR SYGNAŁÓW (Dynamiczny) ---
    with col_agg:
        pair = st.session_state.selected_pair
        info = DATA[pair]
        
        st.subheader(f"📊 Agregator Sygnałów: {pair}")
        
        with st.container():
            st.markdown(f"""<div class="aggregator-box">""", unsafe_allow_html=True)
            
            # 1. Nagłówek i Główne Info
            st.markdown(f"### Instrument: {pair}")
            st.markdown(f"**Źródło pierwotne:** {info['source']} | [Oryginalny wpis]({info['link']})")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Cena Wejścia", info['price'])
            c2.metric("Take Profit", info['tp'], delta_color="normal")
            c3.metric("Stop Loss", info['sl'], delta_color="inverse")
            
            st.divider()

            # 2. Weryfikacja z wielu źródeł (Investing vs TradingView)
            st.write("🔍 **Triple-Source Verification Results:**")
            
            v_col1, v_col2 = st.columns(2)
            
            # Źródło: Investing
            with v_col1:
                v_class = "tag-buy" if "BUY" in info['investing']['verdict'] else "tag-sell"
                st.markdown(f"""
                    <div style="background: #1e222d; padding: 15px; border-radius: 8px;">
                        <b>🔴 Źródło: Investing.com</b><br>
                        Werdykt: <span class="status-tag {v_class}">{info['investing']['verdict']}</span><br>
                        <small>{info['investing']['summary']}</small>
                    </div>
                """, unsafe_allow_html=True)

            # Źródło: TradingView
            with v_col2:
                v_class = "tag-buy" if "BUY" in info['tradingview']['verdict'] else "tag-sell"
                st.markdown(f"""
                    <div style="background: #1e222d; padding: 15px; border-radius: 8px;">
                        <b>🟢 Źródło: TradingView (Zegary)</b><br>
                        Werdykt: <span class="status-tag {v_class}">{info['tradingview']['verdict']}</span><br>
                        <small>{info['tradingview']['summary']}</small>
                    </div>
                """, unsafe_allow_html=True)

            # 3. Werdykt Systemowy
            st.divider()
            if "BUY" in info['investing']['verdict'] and "BUY" in info['tradingview']['verdict']:
                st.success("✅ **ZGODNOŚĆ SYGNAŁÓW (BUY):** Wszystkie źródła potwierdzają wzrosty. Można rozważyć wejście.")
            elif "SELL" in info['investing']['verdict'] and "SELL" in info['tradingview']['verdict']:
                st.error("🚨 **ZGODNOŚĆ SYGNAŁÓW (SELL):** Wszystkie źródła potwierdzają spadki. Można rozważyć krótką pozycję.")
            else:
                st.warning("⚠️ **ROZBIEŻNOŚĆ SYGNAŁÓW:** Źródła podają sprzeczne informacje. Zalecana ostrożność lub czekanie na ujednolicenie trendu.")
            
            st.markdown(f"*Notatka tradera: {info['note']}*")
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
