import streamlit as st

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB SIGNAL HUB V58", page_icon="🎯")

# 2. Stylizacja CSS
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    /* Styl karty po lewej */
    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 20px;
        border-left: 6px solid #3d4451;
        margin-bottom: 20px;
        color: white;
    }
    .buy { border-left-color: #00ff88 !important; }
    .sell { border-left-color: #ff4b4b !important; }
    
    .update-tag { 
        color: #f39c12; 
        font-weight: bold; 
        font-size: 0.85rem; 
        margin-bottom: 10px;
        display: block;
    }
    
    .price-details {
        background: rgba(255,255,255,0.05);
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
    }

    /* Styl agregatora po prawej */
    .aggregator-container {
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 25px;
        position: sticky;
        top: 20px;
    }
    .status-tag { padding: 5px 12px; border-radius: 5px; font-weight: bold; }
    .tag-buy { background-color: rgba(0, 255, 136, 0.2); color: #00ff88; }
    .tag-sell { background-color: rgba(255, 75, 75, 0.2); color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza danych (Dane z Twoich zrzutów ekranu)
DATA = {
    "GOLD": {
        "source": "VasilyTrader",
        "type": "BUY",
        "price": "4509.66",
        "tp": "4525.00",
        "sl": "4495.00",
        "updated": "10.01.2026 15:30",
        "note": "Odbicie od poziomu 4500.",
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
        "updated": "10.01.2026 12:20",
        "note": "Testowanie oporu 1.073.",
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
        "updated": "10.01.2026 06:47",
        "note": "Wybicie z formacji trójkąta.",
        "link": "https://t.me/s/prosignalsfxx",
        "investing": {"verdict": "STRONG BUY", "summary": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "summary": "Średnie: Silne Kupno (12)"}
    }
}

def main():
    st.title("🎯 Terminal Sygnałowy V58 (10.01.2026)")

    if 'active_pair' not in st.session_state:
        st.session_state.active_pair = "GOLD"

    col_left, col_right = st.columns([1, 1])

    # --- PANEL LEWY: PEŁNE DANE SYGNAŁÓW ---
    with col_left:
        st.subheader("📩 Aktywne Sygnały (Pełne Dane)")
        
        for pair, info in DATA.items():
            card_color = "buy" if info["type"] == "BUY" else "sell"
            type_icon = "🟢 KUPNO" if info["type"] == "BUY" else "🔴 SPRZEDAŻ"
            
            # Renderowanie karty po lewej ze wszystkimi danymi
            st.markdown(f"""
                <div class="signal-card {card_color}">
                    <span class="update-tag">🕒 Ostatnia aktualizacja: {info['updated']}</span>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin:0;">{pair}</h3>
                        <b style="color: {'#00ff88' if info['type'] == 'BUY' else '#ff4b4b'}">{type_icon}</b>
                    </div>
                    <p style="margin: 5px 0;">Źródło: <b>{info['source']}</b></p>
                    <div class="price-details">
                        <b>WEJŚCIE:</b> {info['price']}<br>
                        <b>TAKE PROFIT:</b> {info['tp']}<br>
                        <b>STOP LOSS:</b> {info['sl']}
                    </div>
                    <small><i>{info['note']}</i></small>
                </div>
            """, unsafe_allow_html=True)
            
            # Przycisk weryfikacji pod każdą kartą
            if st.button(f"🔎 Weryfikuj {pair} w Agregatorze", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active_pair = pair
                st.rerun()

    # --- PANEL PRAWY: AGREGATOR WERYFIKACYJNY ---
    with col_right:
        selection = st.session_state.active_pair
        item = DATA[selection]
        
        st.subheader(f"📊 Agregator Weryfikacyjny: {selection}")
        
        st.markdown(f"""<div class="aggregator-container">
            <h3>Analiza Wielostronna dla {selection}</h3>
            <p>Porównanie sygnału <b>{item['source']}</b> z danymi rynkowymi.</p>
            <hr style="border-color: #2a2e39;">
        """, unsafe_allow_html=True)
        
        # Investing vs TradingView
        v1, v2 = st.columns(2)
        with v1:
            v_color = "tag-buy" if "BUY" in item['investing']['verdict'] else "tag-sell"
            st.markdown(f"""<div style="background: #1e222d; padding: 15px; border-radius: 8px; min-height: 120px;">
                <b>🔴 Investing.com</b><br>
                Werdykt: <span class="status-tag {v_color}">{item['investing']['verdict']}</span><br><br>
                <small>{item['investing']['summary']}</small>
            </div>""", unsafe_allow_html=True)
            
        with v2:
            v_color = "tag-buy" if "BUY" in item['tradingview']['verdict'] else "tag-sell"
            st.markdown(f"""<div style="background: #1e222d; padding: 15px; border-radius: 8px; min-height: 120px;">
                <b>🟢 TradingView Zegary</b><br>
                Werdykt: <span class="status-tag {v_color}">{item['tradingview']['verdict']}</span><br><br>
                <small>{item['tradingview']['summary']}</small>
            </div>""", unsafe_allow_html=True)

        st.divider()
        
        # Logika Werdyktu Końcowego
        if "BUY" in item['investing']['verdict'] and "BUY" in item['tradingview']['verdict']:
            st.success(f"✅ **ZGODNOŚĆ:** Wszystkie systemy potwierdzają KUPNO {selection}.")
        elif "SELL" in item['investing']['verdict'] and "SELL" in item['tradingview']['verdict']:
            st.error(f"🚨 **ZGODNOŚĆ:** Wszystkie systemy potwierdzają SPRZEDAŻ {selection}.")
        else:
            st.warning("⚠️ **ROZBIEŻNOŚĆ:** Brak jednoznacznego potwierdzenia trendu.")

        st.markdown(f"""<br><a href="{item['link']}" target="_blank" style="color:#37a6ef; text-decoration:none;">🔗 Otwórz oryginalny wpis na Telegramie</a>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
