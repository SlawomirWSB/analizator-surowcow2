import streamlit as st

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB SIGNAL HUB V57", page_icon="🎯")

# 2. Stylizacja CSS
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3d4451;
        margin-bottom: 10px;
        color: white;
    }
    .buy { border-left-color: #00ff88 !important; }
    .sell { border-left-color: #ff4b4b !important; }
    .aggregator-box {
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 20px;
    }
    .status-tag { padding: 5px 10px; border-radius: 5px; font-weight: bold; }
    .tag-buy { background-color: rgba(0, 255, 136, 0.2); color: #00ff88; }
    .tag-sell { background-color: rgba(255, 75, 75, 0.2); color: #ff4b4b; }
    .update-time { color: #f39c12; font-weight: bold; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. Rozszerzona baza danych o godziny aktualizacji
DATA = {
    "GOLD": {
        "source": "VasilyTrader",
        "type": "BUY",
        "price": "4509.66",
        "tp": "4525.00",
        "sl": "4495.00",
        "updated": "10.01.2026 15:30", # Przybliżona godzina z wykresu
        "note": "Odbicie od psychologicznego poziomu 4500.",
        "link": "https://t.me/s/VasilyTrading",
        "investing": {"verdict": "STRONG SELL", "summary": "Wskaźniki: Sell (5) / Buy (2)"},
        "tradingview": {"verdict": "STRONG BUY", "summary": "Średnie kroczące: Silne Kupno (13)"}
    },
    "GBP/CHF": {
        "source": "SignalProvider",
        "type": "SELL",
        "price": "1.073",
        "tp": "1.071",
        "sl": "1.075",
        "updated": "10.01.2026 12:20", # Dokładna godzina z Twojego screena
        "note": "Rynek testuje opór horyzontalny.",
        "link": "https://t.me/s/signalsproviderfx/410",
        "investing": {"verdict": "SELL", "summary": "Wskaźniki: Sell (5) / Buy (1)"},
        "tradingview": {"verdict": "NEUTRAL", "summary": "Podsumowanie: Neutralne (7)"}
    },
    "CAD/JPY": {
        "source": "ProSignalsFx",
        "type": "BUY",
        "price": "113.85",
        "tp": "114.50",
        "sl": "113.30",
        "updated": "10.01.2026 06:47", # Godzina widoczna na Twoim screenie CADJPY
        "note": "Wybicie z formacji trójkąta.",
        "link": "https://t.me/s/prosignalsfxx",
        "investing": {"verdict": "STRONG BUY", "summary": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "summary": "Średnie: Silne Kupno (12)"}
    }
}

def main():
    st.title("🎯 Terminal: Agregator Sygnałów (10.01.2026)")

    # Ustawienie domyślnego wyboru, jeśli nie istnieje
    if 'active_pair' not in st.session_state:
        st.session_state.active_pair = "GOLD"

    col_feed, col_agg = st.columns([1, 1.2])

    # --- PANEL LEWY ---
    with col_feed:
        st.subheader("📡 Sygnały Live")
        for pair, info in DATA.items():
            card_style = "buy" if info["type"] == "BUY" else "sell"
            
            # Kontener karty
            with st.container():
                st.markdown(f"""<div class="signal-card {card_style}">
                    <b style="font-size: 1.1rem;">{pair}</b> | {info['source']}
                </div>""", unsafe_allow_html=True)
                
                # Przycisk weryfikacji (aktualizuje session_state)
                if st.button(f"🔍 Weryfikuj {pair}", key=f"btn_{pair}", use_container_width=True):
                    st.session_state.active_pair = pair
                    st.rerun() # Wymuszenie odświeżenia widoku

    # --- PANEL PRAWY ---
    with col_agg:
        selection = st.session_state.active_pair
        item = DATA[selection]
        
        st.subheader(f"📊 Agregator: {selection}")
        
        st.markdown(f"""<div class="aggregator-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3>Instrument: {selection}</h3>
                <span class="update-time">🕒 Ostatnia aktualizacja: {item['updated']}</span>
            </div>
            <p><b>Źródło pierwotne:</b> {item['source']} | <a href="{item['link']}" style="color:#37a6ef">Oryginalny wpis</a></p>
        """, unsafe_allow_html=True)
        
        # Metryki
        m1, m2, m3 = st.columns(3)
        m1.metric("Wejście", item['price'])
        m2.metric("TP", item['tp'])
        m3.metric("SL", item['sl'])
        
        st.divider()
        st.write("🔍 **Triple-Source Verification Results:**")
        
        v1, v2 = st.columns(2)
        with v1:
            v_color = "tag-buy" if "BUY" in item['investing']['verdict'] else "tag-sell"
            st.markdown(f"""<div style="background: #1e222d; padding: 15px; border-radius: 8px;">
                <b>🔴 Investing.com</b><br>
                Werdykt: <span class="status-tag {v_color}">{item['investing']['verdict']}</span><br>
                <small>{item['investing']['summary']}</small>
            </div>""", unsafe_allow_html=True)
            
        with v2:
            v_color = "tag-buy" if "BUY" in item['tradingview']['verdict'] else "tag-sell"
            st.markdown(f"""<div style="background: #1e222d; padding: 15px; border-radius: 8px;">
                <b>🟢 TradingView Zegary</b><br>
                Werdykt: <span class="status-tag {v_color}">{item['tradingview']['verdict']}</span><br>
                <small>{item['tradingview']['summary']}</small>
            </div>""", unsafe_allow_html=True)

        st.divider()
        # Werdykt automatyczny
        if "BUY" in item['investing']['verdict'] and "BUY" in item['tradingview']['verdict']:
            st.success(f"✅ **ZGODNOŚĆ (KUPNO):** Obie analizy techniczne potwierdzają kierunek {item['source']}.")
        elif "SELL" in item['investing']['verdict'] and "SELL" in item['tradingview']['verdict']:
            st.error(f"🚨 **ZGODNOŚĆ (SPRZEDAŻ):** Obie analizy techniczne potwierdzają kierunek {item['source']}.")
        else:
            st.warning("⚠️ **ROZBIEŻNOŚĆ:** Investing i TradingView mają sprzeczne sygnały. Zalecana ostrożność.")

        st.info(f"📝 **Notatka:** {item['note']}")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
