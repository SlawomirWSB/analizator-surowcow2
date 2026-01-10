import streamlit as st

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB SIGNAL HUB V63", page_icon="📈")

# 2. Stylizacja CSS dla maksymalnej czytelności
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
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
        font-size: 1.1rem;
    }
    .aggregator-container {
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 12px;
        padding: 30px;
        position: sticky;
        top: 20px;
    }
    .status-large { display: block; font-size: 2.2rem; font-weight: 900; margin-top: 10px; }
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
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Dynamiczna Baza Danych (Synchronizowana ze screenami z 10.01.2026)
# Tutaj w przyszłości można dodać funkcję pobierającą dane automatycznie
DATA = {
    "GBP/CHF": {
        "source": "SignalProvider",
        "type": "SELL",
        "price": "1.073",
        "tp": "1.071",
        "sl": "1.075",
        "updated": "10.01.2026 12:20",
        "note": "Rynek testuje opór 1.073. Spodziewany spadek do 1.071.",
        "link": "https://t.me/s/signalsproviderfx",
        "investing": {"verdict": "SELL", "color": "#ff4b4b", "summary": "Wskaźniki: Sell (5) / Buy (1)"},
        "tradingview": {"verdict": "NEUTRAL", "color": "#8f94a1", "summary": "Podsumowanie: Neutralne (7)"}
    },
    "GBP/AUD": {
        "source": "SignalProvider",
        "type": "BUY",
        "price": "2.003",
        "tp": "2.007",
        "sl": "1.998",
        "updated": "10.01.2026 12:30",
        "note": "Cena oscyluje wokół struktury 2.003. Target osiągnie 2.007.",
        "link": "https://t.me/s/signalsproviderfx",
        "investing": {"verdict": "BUY", "color": "#00ff88", "summary": "Wskaźniki: Buy (6) / Sell (2)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "summary": "Zegary: Silne Kupno (11)"}
    },
    "CAD/JPY": {
        "source": "ProSignalsFx",
        "type": "BUY",
        "price": "113.85",
        "tp": "114.50",
        "sl": "113.30",
        "updated": "10.01.2026 06:47",
        "note": "CADJPY is unstoppable. Wybicie z formacji trójkąta (kompresja).",
        "link": "https://t.me/s/prosignalsfxx",
        "investing": {"verdict": "STRONG BUY", "color": "#00ff88", "summary": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "summary": "Zegary: Kupno (12)"}
    }
}

def main():
    st.title("🛡️ Terminal Agregujący V63 (Data: 10.01.2026)")
    st.info("System zsynchronizowany ze źródłami Telegram (Web View). Błędne sygnały (GOLD) zostały usunięte.")

    # Inicjalizacja stanu sesji
    if 'active_pair' not in st.session_state:
        st.session_state.active_pair = list(DATA.keys())[0]

    col_left, col_right = st.columns([1, 1])

    # --- PANEL LEWY: LISTA SYGNAŁÓW ---
    with col_left:
        st.subheader("📩 Aktywne Sygnały (Pełne Dane)")
        for pair, info in DATA.items():
            card_class = "buy" if info["type"] == "BUY" else "sell"
            st.markdown(f"""
                <div class="signal-card {card_class}">
                    <span class="update-tag">🕒 Ostatnia aktualizacja: {info['updated']}</span>
                    <h3 style="margin:0;">{pair} | {info['source']}</h3>
                    <div class="price-details">
                        <b>WEJŚCIE:</b> {info['price']} | <b>TP:</b> {info['tp']} | <b>SL:</b> {info['sl']}
                    </div>
                    <small><i>Status: {info['note']}</i></small>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔎 Weryfikuj {pair}", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active_pair = pair
                st.rerun()

    # --- PANEL PRAWY: AGREGATOR WERYFIKACYJNY ---
    with col_right:
        item = DATA[st.session_state.active_pair]
        st.subheader(f"📊 Agregat Weryfikacyjny: {st.session_state.active_pair}")
        
        st.markdown(f"""<div class="aggregator-container">
            <h2 style="margin:0;">{st.session_state.active_pair} ({item['source']})</h2>
            <hr style="border-color: #2a2e39; margin: 15px 0;">
        """, unsafe_allow_html=True)
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.markdown(f"""<div style="background: #1e222d; padding: 20px; border-radius: 10px; border: 1px solid #2a2e39; text-align: center; min-height: 150px;">
                <b style="color:#ff4b4b;">Investing.com</b><br>
                <span class="status-large" style="color:{item['investing']['color']}">{item['investing']['verdict']}</span><br>
                <small style="color:#8f94a1;">{item['investing']['summary']}</small>
            </div>""", unsafe_allow_html=True)
        with v_col2:
            st.markdown(f"""<div style="background: #1e222d; padding: 20px; border-radius: 10px; border: 1px solid #2a2e39; text-align: center; min-height: 150px;">
                <b style="color:#00ff88;">TradingView</b><br>
                <span class="status-large" style="color:{item['tradingview']['color']}">{item['tradingview']['verdict']}</span><br>
                <small style="color:#8f94a1;">{item['tradingview']['summary']}</small>
            </div>""", unsafe_allow_html=True)

        # Przycisk do źródła
        st.markdown(f"""
            <a href="{item['link']}" target="_blank" class="btn-telegram">
                ✈️ Otwórz źródło {item['source']} (Prawidłowy Web View)
            </a>
        """, unsafe_allow_html=True)
        
        # Logika werdyktu zbiorczego
        st.markdown("<br>", unsafe_allow_html=True)
        if (item['type'] in item['investing']['verdict']) and (item['type'] in item['tradingview']['verdict']):
            st.success(f"✅ **ZGODNOŚĆ:** Oba systemy potwierdzają kierunek {item['type']} dla {st.session_state.active_pair}.")
        else:
            st.warning("⚠️ **UWAGA:** Brak pełnej zgodności między sygnałem a wskaźnikami technicznymi.")
            
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
