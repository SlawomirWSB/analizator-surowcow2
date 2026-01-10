import streamlit as st
from datetime import datetime

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB SIGNAL DASHBOARD V51", page_icon="📈")

# 2. Stylizacja kart sygnałów (CSS)
st.markdown("""
    <style>
    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #3d4451;
        margin-bottom: 20px;
        color: white;
    }
    .buy { border-left: 5px solid #00ff88; }
    .sell { border-left: 5px solid #ff4b4b; }
    .signal-header { font-size: 1.2rem; font-weight: bold; margin-bottom: 5px; }
    .price { color: #8f94a1; font-family: monospace; }
    .tp { color: #00ff88; font-weight: bold; }
    .sl { color: #ff4b4b; font-weight: bold; }
    .meta { font-size: 0.8rem; color: #5d6270; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza danych sygnałów (To możesz aktualizować ręcznie lub przez API)
SIGNALS = [
    {
        "channel": "SignalProvider",
        "instrument": "GOLD (Złoto)",
        "type": "BUY",
        "entry": "2042.00",
        "tp": "2045.00 / 2050.00",
        "sl": "2035.00",
        "date": "10.01.2026 09:15",
        "note": "Złoto utrzymuje się powyżej wsparcia. Wejście rynkowe."
    },
    {
        "channel": "VasilyTrader",
        "instrument": "GOLD (Złoto)",
        "type": "BUY",
        "entry": "2040.50",
        "tp": "2055.00",
        "sl": "2032.00",
        "date": "10.01.2026 10:30",
        "note": "Fałszywe wybicie na H1. Wysokie prawdopodobieństwo."
    },
    {
        "channel": "TopTradingSignals",
        "instrument": "EUR/USD",
        "type": "SELL",
        "entry": "1.0945",
        "tp": "1.0910",
        "sl": "1.0980",
        "date": "10.01.2026 08:45",
        "note": "Oczekiwanie na umocnienie dolara przed danymi z USA."
    },
    {
        "channel": "ProSignalsFX",
        "instrument": "GBP/USD",
        "type": "BUY",
        "entry": "1.2720",
        "tp": "1.2760",
        "sl": "1.2680",
        "date": "10.01.2026 11:00",
        "note": "Przesuń SL na BE po osiągnięciu +15 pipsów."
    }
]

def main():
    st.title("🎯 Terminal Sygnałowy (Darmowe Sygnały)")
    st.write(f"Ostatnia aktualizacja danych: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    
    # Filtry na górze
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_instr = st.multiselect("Filtruj Instrument:", ["GOLD (Złoto)", "EUR/USD", "GBP/USD"], default=["GOLD (Złoto)", "EUR/USD", "GBP/USD"])
    
    st.markdown("---")

    # Wyświetlanie kart w układzie siatki (2 kolumny)
    cols = st.columns(2)
    for i, sig in enumerate(SIGNALS):
        if sig["instrument"] in f_instr:
            # Wybór kolumny (lewa/prawa)
            target_col = cols[i % 2]
            
            # Stylizacja w zależności od typu (Kupno/Sprzedaż)
            card_class = "buy" if sig["type"] == "BUY" else "sell"
            type_pl = "🟢 KUPNO" if sig["type"] == "BUY" else "🔴 SPRZEDAŻ"
            
            with target_col:
                st.markdown(f"""
                    <div class="signal-card {card_class}">
                        <div class="signal-header">{sig['instrument']} - {type_pl}</div>
                        <div>Źródło: <b>{sig['channel']}</b></div>
                        <div class="price">Wejście: {sig['entry']}</div>
                        <hr style="border: 0.1px solid #2a2e39; margin: 10px 0;">
                        <div>🎯 <span class="tp">TP: {sig['tp']}</span></div>
                        <div>🛡️ <span class="sl">SL: {sig['sl']}</span></div>
                        <div class="meta">
                            <i>{sig['note']}</i><br>
                            📅 {sig['date']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
