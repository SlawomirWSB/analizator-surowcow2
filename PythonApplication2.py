import streamlit as st

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB SIGNAL HUB V59", page_icon="🎯")

# 2. Stylizacja CSS dla lepszej czytelności
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    
    /* Lewy Panel - Karty Sygnałów */
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
        margin-bottom: 8px;
        display: block;
    }
    
    .price-details {
        background: rgba(255,255,255,0.07);
        padding: 12px;
        border-radius: 8px;
        margin: 12px 0;
        font-family: 'Courier New', monospace;
        font-size: 1.05rem;
    }

    /* Prawy Panel - Agregator */
    .aggregator-container {
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 12px;
        padding: 30px;
        position: sticky;
        top: 20px;
    }
    
    .verdict-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
    }
    
    .status-large { 
        display: block;
        font-size: 1.8rem; 
        font-weight: 900; 
        margin-top: 5px;
    }

    .btn-telegram {
        display: inline-block;
        padding: 10px 20px;
        background-color: #0088cc;
        color: white !important;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 15px;
        text-align: center;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza danych (Dane z Twoich zrzutów ekranu - Jan 10)
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
        "investing": {"verdict": "STRONG SELL", "color": "#ff4b4b", "summary": "Wskaźniki: Sell (5) / Buy (2)"},
        "tradingview": {"verdict": "STRONG BUY", "color": "#00ff88", "summary": "Średnie kroczące: Silne Kupno (13)"}
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
        "investing": {"verdict": "SELL", "color": "#ff4b4b", "summary": "Wskaźniki: Sell (5) / Buy (1)"},
        "tradingview": {"verdict": "NEUTRAL", "color": "#8f94a1", "summary": "Podsumowanie: Neutralne (7)"}
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
        "investing": {"verdict": "STRONG BUY", "color": "#00ff88", "summary": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "summary": "Średnie: Silne Kupno (12)"}
    }
}

def main():
    st.title("🎯 Terminal Sygnałowy V59 (Jan 10, 2026)")

    if 'active_pair' not in st.session_state:
        st.session_state.active_pair = "GOLD"

    col_left, col_right = st.columns([1, 1])

    # --- PANEL LEWY: PEŁNE DANE SYGNAŁÓW ---
    with col_left:
        st.subheader("📩 Sygnały Live (Telegram)")
        
        for pair, info in DATA.items():
            card_class = "buy" if info["type"] == "BUY" else "sell"
            type_label = "🟢 KUPNO" if info["type"] == "BUY" else "🔴 SPRZEDAŻ"
            
            st.markdown(f"""
                <div class="signal-card {card_class}">
                    <span class="update-tag">🕒 Aktualizacja: {info['updated']}</span>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin:0;">{pair}</h3>
                        <b style="color: {'#00ff88' if info['type'] == 'BUY' else '#ff4b4b'}">{type_label}</b>
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
            
            if st.button(f"🔎 Analizuj {pair}", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active_pair = pair
                st.rerun()

    # --- PANEL PRAWY: POPRAWIONY AGREGATOR ---
    with col_right:
        item = DATA[st.session_state.active_pair]
        
        st.subheader(f"📊 Agregator Weryfikacyjny: {st.session_state.active_pair}")
        
        st.markdown(f"""<div class="aggregator-container">
            <h2 style="margin-bottom:0;">{st.session_state.active_pair}</h2>
            <p style="color:#8f94a1;">Weryfikacja techniczna dla sygnału od <b>{item['source']}</b></p>
            <hr style="border-color: #2a2e39; margin: 20px 0;">
        """, unsafe_allow_html=True)
        
        # Sekcja werdyktów (Investing i TradingView)
        v_col1, v_col2 = st.columns(2)
        
        with v_col1:
            st.markdown(f"""
                <div style="background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #2a2e39;">
                    <b style="color:#ff4b4b;">🔴 Investing.com</b><br>
                    <span class="status-large" style="color:{item['investing']['color']}">{item['investing']['verdict']}</span>
                    <hr style="border-color: #2a2e39; margin: 10px 0;">
                    <small style="color:#8f94a1;">{item['investing']['summary']}</small>
                </div>
            """, unsafe_allow_html=True)
            
        with v_col2:
            st.markdown(f"""
                <div style="background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #2a2e39;">
                    <b style="color:#00ff88;">🟢 TradingView</b><br>
                    <span class="status-large" style="color:{item['tradingview']['color']}">{item['tradingview']['verdict']}</span>
                    <hr style="border-color: #2a2e39; margin: 10px 0;">
                    <small style="color:#8f94a1;">{item['tradingview']['summary']}</small>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Werdykt Zbiorczy
        if "BUY" in item['investing']['verdict'] and "BUY" in item['tradingview']['verdict']:
            st.success("✅ **PEŁNA ZGODNOŚĆ:** Wszystkie systemy potwierdzają kierunek wzrostowy.")
        elif "SELL" in item['investing']['verdict'] and "SELL" in item['tradingview']['verdict']:
            st.error("🚨 **PEŁNA ZGODNOŚĆ:** Wszystkie systemy potwierdzają kierunek spadkowy.")
        else:
            st.warning("⚠️ **ROZBIEŻNOŚĆ:** Systemy techniczne nie są zgodne. Zachowaj ostrożność.")

        # Przycisk do oryginalnej treści
        st.markdown(f"""
            <hr style="border-color: #2a2e39; margin: 25px 0;">
            <b>Weryfikacja źródła:</b>
            <a href="{item['link']}" target="_blank" class="btn-telegram">
                ✈️ Otwórz oryginalny sygnał na Telegramie
            </a>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
