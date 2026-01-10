import streamlit as st

st.set_page_config(layout="wide", page_title="Sygnały 10.01.2026")

def signal_card(title, direction, entry, tp, sl, note, link, color):
    st.markdown(f"""
        <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid {color}; margin-bottom: 20px; color: white;">
            <h4>{title}</h4>
            <p><b>Kierunek:</b> {direction}</p>
            <p><b>Wejście:</b> {entry} | <b>TP:</b> {tp} | <b>SL:</b> {sl}</p>
            <p style="font-size: 0.9em; color: #8f94a1;"><i>{note}</i></p>
            <a href="{link}" target="_blank" style="color: #37a6ef; text-decoration: none;">🔗 Zobacz oryginalny wpis</a>
        </div>
    """, unsafe_allow_html=True)

st.title("🎯 Aktywne Sygnały: 10 Stycznia 2026")

c1, c2 = st.columns(2)
with c1:
    signal_card("🥇 GOLD - VasilyTrader", "🟢 KUPNO (BUY)", "ok. 4509", "4525", "4495", "Odbicie od poziomu 4500. Potwierdzone przez zegary TV.", "https://t.me/s/VasilyTrading", "#00ff88")
    signal_card("📉 GBP/CHF - SignalProvider", "🔴 SPRZEDAŻ (SELL)", "1.073", "1.071", "1.075", "Testowanie oporu horyzontalnego.", "https://t.me/s/signalsproviderfx/410", "#ff4b4b")

with c2:
    signal_card("🥇 GOLD - ProSignalsFX", "🟢 KUPNO (BUY)", "Market", "4520", "4500", "Trend wzrostowy utrzymany na interwale 15m.", "https://t.me/s/prosignalsfxx", "#00ff88")
    st.info("💡 **TopTradingSignals**: Obecnie brak nowych darmowych sygnałów z parametrami. Ostatnie wpisy to analizy rynkowe.")
