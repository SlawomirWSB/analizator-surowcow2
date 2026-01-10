import streamlit as st

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB SIGNAL HUB V60", page_icon="📈")

# 2. Stylizacja CSS
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    
    /* Lewy Panel */
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
    
    .update-tag { color: #f39c12; font-weight: bold; font-size: 0.85rem; margin-bottom: 8px; display: block; }
    
    .price-details {
        background: rgba(255,255,255,0.07);
        padding: 12px;
        border-radius: 8px;
        margin: 12px 0;
        font-family: 'Courier New', monospace;
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
    
    .status-large { 
        display: block;
        font-size: 2rem; 
        font-weight: 900; 
        margin-top: 10px;
    }

    .btn-telegram {
        display: block;
        padding: 15px;
        background-color: #0088cc;
        color: white !important;
        text-decoration: none !important;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 20px;
        text-align: center;
        font-size: 1.1rem;
        transition: 0.3s;
    }
    .btn-telegram:hover { background-color: #00aaff; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza danych z linkami do konkretnych wiadomości
DATA = {
    "GOLD": {
        "source": "VasilyTrader",
        "type": "BUY",
        "price": "4509.66",
        "tp": "4525.00",
        "sl": "4495.00",
        "updated": "10.01.2026 15:30",
        "note": "Odbicie od poziomu 4500.",
        "link": "https://t.me/VasilyTrading", # Link ogólny kanału
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
        "link": "https://t.me/signalsproviderfx/410", # Bezpośredni link do wiadomości
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
        "link": "https://t.me/prosignalsfxx/552", # Bezpośredni link do wiadomości
        "investing": {"verdict": "STRONG BUY", "color": "#00ff88", "summary": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "summary": "Średnie: Silne Kupno (12)"}
    }
}

def main():
    st.title("🛡️ Terminal Agregujący V60 (10.01.2026)")

    if 'active_pair' not in st.session_state:
        st.session_state.active_pair = "GOLD"

    col_left, col_right = st.columns([1, 1])

    # --- PANEL LEWY ---
    with col_left:
        st.subheader("📩 Sygnały z Twoich Źródeł")
        for pair, info in DATA.items():
            card_class = "buy" if info["type"] == "BUY" else "sell"
            st.markdown(f"""
                <div class="signal-card {card_class}">
                    <span class="update-tag">🕒 Aktualizacja: {info['updated']}</span>
                    <h3 style="margin:0;">{pair} | {info['source']}</h3>
                    <div class="price-details">
                        <b>WEJŚCIE:</b> {info['price']} | <b>TP:</b> {info['tp']} | <b>SL:</b> {info['sl']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔍 Weryfikuj i Agreguj {pair}", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active_pair = pair
                st.rerun()

    # --- PANEL PRAWY: AGREGATOR ---
    with col_right:
        item = DATA[st.session_state.active_pair]
        
        st.subheader(f"📊 Agregat Danych: {st.session_state.active_pair}")
        
        st.markdown(f"""<div class="aggregator-container">
            <h2 style="margin:0;">{st.session_state.active_pair} Analysis</h2>
            <hr style="border-color: #2a2e39; margin: 15px 0;">
        """, unsafe_allow_html=True)
        
        # Sekcja werdyktów technicznych
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.markdown(f"""
                <div style="background: #1e222d; padding: 20px; border-radius: 10px; border: 1px solid #2a2e39; text-align: center;">
                    <b style="color:#ff4b4b;">Investing.com</b><br>
                    <span class="status-large" style="color:{item['investing']['color']}">{item['investing']['verdict']}</span>
                </div>
            """, unsafe_allow_html=True)
        with v_col2:
            st.markdown(f"""
                <div style="background: #1e222d; padding: 20px; border-radius: 10px; border: 1px solid #2a2e39; text-align: center;">
                    <b style="color:#00ff88;">TradingView</b><br>
                    <span class="status-large" style="color:{item['tradingview']['color']}">{item['tradingview']['verdict']}</span>
                </div>
            """, unsafe_allow_html=True)

        # Przycisk linkujący do konkretnej wiadomości
        st.markdown(f"""
            <a href="{item['link']}" target="_blank" class="btn-telegram">
                ✈️ Otwórz oryginalny sygnał na Telegramie ({item['source']})
            </a>
            <p style="margin-top:20px; color:#8f94a1;"><i>Notatka: {item['note']}</i></p>
        """, unsafe_allow_html=True)
        
        # Podsumowanie zgodności
        if "BUY" in item['investing']['verdict'] and "BUY" in item['tradingview']['verdict']:
            st.success("✅ Pełna zgodność systemów (KUPNO)")
        elif "SELL" in item['investing']['verdict'] and "SELL" in item['tradingview']['verdict']:
            st.error("🚨 Pełna zgodność systemów (SPRZEDAŻ)")
        else:
            st.warning("⚠️ Brak zgodności wskaźników technicznych")

        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
