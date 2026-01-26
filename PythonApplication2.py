import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import yfinance as yf
import time

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V6.5 - Multi-Asset", layout="wide")

# LISTY INSTRUMENTÓW
KRYPTO = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "LINK/USDT", "MATIC/USDT", "XRP/USDT"]
ZASOBY = {
    "Złoto": "GC=F",
    "Srebro": "SI=F",
    "Ropa WTI": "CL=F",
    "Kakao": "CC=F",
    "EUR/PLN": "EURPLN=X",
    "USD/PLN": "USDPLN=X",
    "EUR/USD": "EURUSD=X"
}

interval_map_krypto = {"5 min": "5m", "15 min": "15m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}
interval_map_yf = {"5 min": "5m", "15 min": "15m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

# --- POBIERANIE DANYCH ---
@st.cache_data(ttl=300)
def pobierz_krypto(int_label):
    ex = ccxt.binanceus()
    data = {}
    tf = interval_map_krypto[int_label]
    for sym in KRYPTO:
        try:
            ohlcv = ex.fetch_ohlcv(sym, timeframe=tf, limit=150)
            df = pd.DataFrame(ohlcv, columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            data[sym] = df.set_index(pd.to_datetime(df['time'], unit='ms'))
            time.sleep(0.02)
        except: continue
    return data

@st.cache_data(ttl=300)
def pobierz_zasoby(int_label):
    data = {}
    tf = interval_map_yf[int_label]
    for nazwa, ticker in ZASOBY.items():
        try:
            df = yf.download(ticker, period="1mo", interval=tf, progress=False)
            if not df.empty:
                data[nazwa] = df
        except: continue
    return data

# --- ANALIZA (Zaszyta logika V6.2) ---
def analizuj(df, kapital_pln, mode):
    try:
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.macd(append=True)
        df.ta.stochrsi(length=14, append=True)
        df['Vol_Avg'] = df['Volume'].rolling(20).mean()
        
        l = df.iloc[-1]
        c, e, a, r, atr = float(l['Close']), float(l['EMA_20']), float(l['ADX_14']), float(l['RSI_14']), float(l['ATRr_14'])
        macd_h = float(l['MACDh_12_26_9'])
        stoch_k = float(l['STOCHRSIk_14_14_3_3'])
        vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1.0
        
        sig = "KUP" if c > e else "SPRZEDAJ"
        if a < 20: sig = "KONSOLIDACJA"
        
        wej = c if mode == "rynkowy" else e
        sl_dist = atr * 1.5
        ilosc = (kapital_pln * 0.01) / (sl_dist * 4.0) # Uproszczony kurs USDPLN
        
        return {
            "Sygnał": sig, "Siła %": min(98, 40 + (20 if a > 25 else 0)),
            "Cena": round(c, 4), "RSI": round(r, 1), "StochRSI": round(stoch_k, 1),
            "Pęd": "Wzrost" if macd_h > 0 else "Spadek", "ADX": round(a, 1),
            "Wolumen %": round(vol_ratio * 100), "Ile kupić (1%)": round(ilosc, 4),
            "TP": round(wej + (atr*2.5) if sig=="KUP" else wej - (atr*2.5), 4),
            "SL": round(wej - sl_dist if sig=="KUP" else wej + sl_dist, 4)
        }
    except: return None

# --- STYLIZACJA ---
def stylizuj(row):
    s = [''] * len(row)
    sig, rsi, stoch = row['Sygnał'], row['RSI'], row['StochRSI']
    if sig == 'KUP': s[1] = 'background-color: #1e4620; color: white'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #5f1a1d; color: white'
    if sig == 'KUP': s[4] = 'color: #00ff00' if rsi < 50 else 'color: #ff4b4b'
    elif sig == 'SPRZEDAJ': s[4] = 'color: #00ff00' if rsi > 50 else 'color: #ff4b4b'
    if (sig == 'KUP' and stoch < 20) or (sig == 'SPRZEDAJ' and stoch > 80): s[5] = 'background-color: #007d00; color: white'
    elif (sig == 'KUP' and stoch > 80) or (sig == 'SPRZEDAJ' and stoch < 20): s[5] = 'background-color: #7d0000; color: white'
    s[6] = 'color: #00ff00' if row['Pęd'] == 'Wzrost' else 'color: #ff4b4b'
    s[7] = 'color: #00ff00; font-weight: bold' if row['ADX'] > 25 else 'color: #ff4b4b'
    return s

# --- INTERFEJS ---
st.title("🌍 Skaner PRO V6.5 - Krypto, Surowce & Forex")

with st.sidebar:
    st.header("Portfel")
    user_kapital = st.number_input("Kapitał (PLN):", value=10000)
    wybrany_int = st.select_slider("Interwał:", options=list(interval_map_krypto.keys()), value="4 godz")
    tryb = st.radio("Cena wejścia:", ["Rynkowa", "Limit (EMA20)"])

tab_k, tab_z = st.tabs(["₿ KRYPTOWALUTY", "🥇 SUROWCE I FOREX"])

with tab_k:
    dane_k = pobierz_krypto(wybrany_int)
    wyniki = []
    for s, df in dane_k.items():
        res = analizuj(df, user_kapital, tryb.lower())
        if res: wyniki.append({"Instrument": s, **res})
    if wyniki:
        st.dataframe(pd.DataFrame(wyniki).style.apply(stylizuj, axis=1), use_container_width=True)

with tab_z:
    dane_z = pobierz_zasoby(wybrany_int)
    wyniki_z = []
    for s, df in dane_z.items():
        res = analizuj(df, user_kapital, tryb.lower())
        if res: wyniki_z.append({"Instrument": s, **res})
    if wyniki_z:
        st.dataframe(pd.DataFrame(wyniki_z).style.apply(stylizuj, axis=1), use_container_width=True)
