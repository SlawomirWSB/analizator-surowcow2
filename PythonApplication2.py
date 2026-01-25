import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Rozszerzona lista krypto dostępnych na XTB
KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", 
    "UNI-USD", "ATOM-USD", "ETC-USD", "XMR-USD", "ALGO-USD", "AAVE-USD", "VET-USD"
]

interval_map = {"1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

def oblicz_score(cena, ema20, ema50, rsi, macd, macds, adx):
    """Uniwersalna funkcja licząca siłę sygnału 0-100%"""
    buy_score = 30 # Baza
    # Trend
    if cena > ema20: buy_score += 15
    if ema20 > ema50: buy_score += 10
    # Momentum
    if macd > macds: buy_score += 15
    if rsi < 40: buy_score += 15
    if adx > 25: buy_score += 15
    
    sell_score = 30
    if cena < ema20: sell_score += 15
    if ema20 < ema50: sell_score += 10
    if macd < macds: sell_score += 15
    if rsi > 60: sell_score += 15
    if adx > 25: sell_score += 15
    
    if buy_score >= sell_score:
        return "KUP", min(buy_score, 98)
    else:
        return "SPRZEDAJ", min(sell_score, 98)

def wykonaj_skan(tryb="rynkowy", interwal_label="4 godz"):
    wyniki = []
    interwal = interval_map[interwal_label]
    
    for symbol in KRYPTO_XTB:
        try:
            df = yf.download(symbol, period="100d", interval=interwal, progress=False)
            if df.empty or len(df) < 50: continue
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            # Wskaźniki techniczne
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.ema(length=50, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.macd(append=True)
            df.ta.adx(append=True)

            l = df.iloc[-1]
            cena_r = float(l['Close'])
            sig, power = oblicz_score(cena_r, l['EMA_20'], l['EMA_50'], l['RSI_14'], 
                                     l['MACD_12_26_9'], l['MACDs_12_26_9'], l['ADX_14'])
            
            # Logika wejścia
            if tryb == "rynkowy":
                wejscie = cena_r
            else:
                # Sugerowane: wejście przy korekcie do EMA20 lub 0.5% od ceny
                wejscie = l['EMA_20'] if sig == "KUP" else l['EMA_20']

            atr = l['ATRr_14']
            res = {
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": power,
                "Cena Wejścia": round(wejscie, 4),
                "TP (Cel)": round(wejscie + (atr*2.5) if sig=="KUP" else wejscie - (atr*2.5), 4),
                "SL (Stop)": round(wejscie - (atr*1.5) if sig=="KUP" else wejscie + (atr*1.5), 4),
                "ADX (Trend)": round(l['ADX_14'], 1)
            }
            wyniki.append(res)
        except: continue
    return wyniki

# --- UI ---
st.title("⚖️ Skaner PRO Multi-Tryb")
int_sel = st.select_slider("Interwał:", options=list(interval_map.keys()), value="4 godz")

col1, col2 = st.columns(2)
with col1:
    btn_market = st.button("🚀 ANALIZA - CENA BIEŻĄCA", use_container_width=True)
with col2:
    btn_sug = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

final_data = None
if btn_market:
    final_data = wykonaj_skan("rynkowy", int_sel)
    st.subheader("Wyniki dla wejścia natychmiastowego (Market)")
elif btn_sug:
    final_data = wykonaj_skan("sugerowany", int_sel)
    st.subheader("Wyniki dla wejścia zoptymalizowanego (Limit/Korekta)")

if final_data:
    df = pd.DataFrame(final_data).sort_values(by="Siła %", ascending=False)
    
    def color_sig(val):
        color = '#1e4620' if val == 'KUP' else '#5f1a1d'
        return f'background-color: {color}; color: white'

    st.dataframe(df.style.applymap(color_sig, subset=['Sygnał']), use_container_width=True)
