import streamlit as st

# 1. Konfiguracja interfejsu
st.set_page_config(layout="wide", page_title="XTB HUB V67 - Advanced", page_icon="📊")

st.markdown("""
    <style>
    /* Naprawa czytelności na komputerze - jasne napisy */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    .main-title { font-size: 1.8rem; font-weight: 800; text-align: center; color: #ffffff; margin-bottom: 20px; }

    /* Karta sygnału po lewej - wysoki kontrast */
    .signal-card {
        background-color: #1e222d;
        border: 1px solid #363c4e;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        color: #ffffff !important;
    }
    .pair-title { font-size: 1.3rem; font-weight: bold; color: #ffffff !important; }
    
    /* Agregatory po prawej */
    .aggregator-card {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .time-badge {
        background: #2a2e39;
        color: #f39c12;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    /* Nowy Widget Wizualny (Gauge) */
    .gauge-container {
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin-top: 10px;
    }
    .gauge-point {
        width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Rozszerzona Baza Danych z interwałami
DATA = {
    "GBP/CHF": {
        "source": "SignalProvider", "type": "SPRZEDAŻ", "type_en": "SELL",
        "price": "1.073", "tp": "1.071", "sl": "1.075", "updated": "12:20",
        "investing": {"verdict": "STRONG SELL", "color": "#ff4b4b", "timeframe": "1 Godzina", "summary": "Sell (14) / Neutral (9)"},
        "tradingview": {"verdict": "STRONG SELL", "color": "#ff4b4b", "timeframe": "1 Dzień", "summary": "Średnie: Silna Sprzedaż (13)"},
        "link": "https://t.me/s/signalsproviderfx"
    },
    "GBP/AUD": {
        "source": "SignalProvider", "type": "KUPNO", "type_en": "BUY",
        "price": "2.003", "tp": "2.007", "sl": "1.998", "updated": "12:30",
        "investing": {"verdict": "BUY", "color": "#00ff88", "timeframe": "1 Godzina", "summary": "Buy (6) / Sell (2)"},
        "tradingview": {"verdict": "STRONG BUY", "color": "#00ff88", "timeframe": "1 Dzień", "summary": "Zegary: Kupno (14)"},
        "link": "https://t.me/s/signalsproviderfx"
    },
    "CAD/JPY": {
        "source": "ProSignalsFx", "type": "KUPNO", "type_en": "BUY",
        "price": "113.85", "tp": "114.50", "sl": "113.30", "updated": "06:47",
        "investing": {"verdict": "STRONG BUY", "color": "#00ff88", "timeframe": "1 Godzina", "summary": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "timeframe": "4 Godziny", "summary": "Zegary: Kupno (12)"},
        "link": "https://t.me/s/prosignalsfxx"
    }
}

def render_gauge(label, value, color):
    st.markdown(f"""
        <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px;">
            <small style="color: #b2b5be;">{label}</small>
            <div style="font-size: 1.2rem; font-weight: bold; color: {color};">{value}</div>
            <div style="height: 4px; background: #2a2e39; border-radius: 2px; margin-top: 5px;">
                <div style="width: 80%; height: 100%; background: {color}; border-radius: 2px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-title">Terminal V67 - Agregator Systemowy</div>', unsafe_allow_html=True)

    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"

    col_l, col_r = st.columns([1, 1.3])

    with col_l:
        st.subheader("📩 Sygnały")
        for pair, info in DATA.items():
            border = "#00ff88" if info["type_en"] == "BUY" else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card" style="border-left: 5px solid {border}">
                    <div style="display:flex; justify-content:space-between;">
                        <span class="pair-title">{pair}</span>
                        <span style="background:{border}; color:{'#000' if info['type_en']=='BUY' else '#fff'}; padding:2px 8px; border-radius:4px; font-weight:bold; font-size:0.8rem;">{info['type']}</span>
                    </div>
                    <div style="color:#b2b5be; font-size:0.85rem; margin-top:5px;">Źródło: {info['source']} | Aktualizacja: {info['updated']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Weryfikuj {pair}", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active = pair
                st.rerun()

    with col_r:
        item = DATA[st.session_state.active]
        st.subheader(f"📊 Analiza Multi-Timeframe: {st.session_state.active}")
        
        # Przywrócone dwa agregaty z dodanym interwałem
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="aggregator-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <small style="color:#b2b5be;">Investing.com</small>
                    <span class="time-badge">{item['investing']['timeframe']}</span>
                </div>
                <div style="font-size:1.5rem; font-weight:900; color:{item['investing']['color']}; margin:10px 0;">{item['investing']['verdict']}</div>
                <small style="color:#d1d4dc;">{item['investing']['summary']}</small>
            </div>""", unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""<div class="aggregator-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <small style="color:#b2b5be;">TradingView</small>
                    <span class="time-badge">{item['tradingview']['timeframe']}</span>
                </div>
                <div style="font-size:1.5rem; font-weight:900; color:{item['tradingview']['color']}; margin:10px 0;">{item['tradingview']['verdict']}</div>
                <small style="color:#d1d4dc;">{item['tradingview']['summary']}</small>
            </div>""", unsafe_allow_html=True)

        # NOWY WIDGET: Wizualizacja Zegarów (Gauge Widget)
        st.markdown('<div class="aggregator-card"><small style="color:#b2b5be;">WIDGET ANALITYCZNY (OSCYLATORY & ŚREDNIE)</small>', unsafe_allow_html=True)
        g1, g2, g3 = st.columns(3)
        with g1: render_gauge("Oscylatory", "Neutralnie", "#8f94a1")
        with g2: render_gauge("Podsumowanie", item['tradingview']['verdict'], item['tradingview']['color'])
        with g3: render_gauge("Średnie", "Silna Sprzedaż" if "SELL" in item['tradingview']['verdict'] else "Silne Kupno", item['tradingview']['color'])
        st.markdown('</div>', unsafe_allow_html=True)

        st.link_button(f"✈️ Otwórz źródło na Telegramie", item["link"], use_container_width=True)

if __name__ == "__main__": main()
