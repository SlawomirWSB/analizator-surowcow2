import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import yfinance as yf
import time

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V6.8 - Pełna Edycja", layout="wide")

# ROZSZERZONE LISTY INSTRUMENTÓW
KRYPTO = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "LINK/USDT", "MATIC/USDT", "XRP/USDT", 
          "ADA/USDT", "DOT/USDT", "LTC/USDT", "TRX/USDT", "DOGE/USDT", "AVAX/USDT"]

ZASOBY = {
    "Złoto (GOLD)": "GC=F", "Srebro (SILVER)": "SI=F", "Ropa WTI (OIL)": "CL=F",
    "Miedź (COPPER)": "HG=F", "Gaz (NATGAS)": "NG=F", "Kakao (COCOA)": "CC=F",
    "EUR/PLN": "EURPLN=X", "USD/PLN": "USDPLN=X", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X",
    "S&P 500": "^GSPC", "DAX 40": "^GDAXI"
}

# Rozszerzony zakres interwałów do 1 miesiąca
interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1w", "1 mies": "1mo"
}

# --- FUNKCJE POMOCNICZE ---
@st.cache_data(ttl=300)
def pobierz_krypto(int_label):
    ex = ccxt.binanceus()
    data = {}
    tf = interval_map[int_label]
    if tf == "1mo": tf = "1M" # Korekta dla API Binance
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
    tf = interval_map[int_label]
    for nazwa, ticker in ZASOBY.items():
        try:
            df = yf.download(ticker, period="2y", interval=tf, progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                data[nazwa] = df
        except: continue
    return data

def run_backtest(df):
    if len(df) < 70: return 0.0
    test_data = df.tail(100).copy()
    test_data['EMA'] = ta.ema(test_data['Close'], length=20)
    cap, pos = 1000.0, 0.0
    for i in range(50, len(test_data)):
        p, e = test_data['Close'].iloc[i], test_data['EMA'].iloc[i]
        if p > e and pos == 0: pos = cap / p
        elif p < e and pos > 0: cap, pos = pos * p, 0.0
    final = cap if pos == 0 else pos * test_data['Close'].iloc[-1]
    return round(((final - 1000) / 1000) * 100, 2)

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
        ilosc = (kapital_pln * 0.01) / (sl_dist * 4.0) 
        
        return {
            "Sygnał": sig, "Siła %": min(98, 40 + (20 if a > 25 else 0) + (15 if (sig=="KUP" and macd_h>0) or (sig=="SPRZEDAJ" and macd_h<0) else 0)),
            "Cena": round(c, 4), "RSI": round(r, 1), "StochRSI": round(stoch_k, 1),
            "Pęd": "Wzrost" if macd_h > 0 else "Spadek", "ADX": round(a, 1),
            "Wolumen %": round(vol_ratio * 100), "Ile kupić (1%)": round(ilosc, 4),
            "TP": round(wej + (atr*2.5) if sig=="KUP" else wej - (atr*2.5), 4),
            "SL": round(wej - sl_dist if sig=="KUP" else wej + sl_dist, 4),
            "Hist. 50ś": f"{run_backtest(df)}%"
        }
    except: return None

# --- STYLIZACJA ---
def stylizuj(row):
    s = [''] * len(row)
    sig, rsi, stoch, vol = row['Sygnał'], row['RSI'], row['StochRSI'], row['Wolumen %']
    
    if sig == 'KUP': s[1] = 'background-color: #1e4620; color: white'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #5f1a1d; color: white'
    
    if sig == 'KUP': s[4] = 'color: #00ff00' if rsi < 50 else 'color: #ff4b4b'
    elif sig == 'SPRZEDAJ': s[4] = 'color: #00ff00' if rsi > 50 else 'color: #ff4b4b'
    
    if (sig == 'KUP' and stoch < 20) or (sig == 'SPRZEDAJ' and stoch > 80): s[5] = 'background-color: #007d00; color: white'
    elif (sig == 'KUP' and stoch > 80) or (sig == 'SPRZEDAJ' and stoch < 20): s[5] = 'background-color: #7d0000; color: white'
    
    s[6] = 'color: #00ff00' if row['Pęd'] == 'Wzrost' else 'color: #ff4b4b'
    s[7] = 'color: #00ff00; font-weight: bold' if row['ADX'] > 25 else 'color: #ff4b4b'
    
    # Kolor Wolumenu zależny od potwierdzenia sygnału
    s[8] = 'color: #00ff00' if vol > 110 else 'color: #ff4b4b' if vol < 80 else ''
    
    v_h = float(row['Hist. 50ś'].replace('%',''))
    s[12] = 'color: #00ff00' if v_h > 0 else 'color: #ff4b4b' if v_h < 0 else ''
    return s

# --- INTERFEJS ---
with st.sidebar:
    st.header("⚙️ Ustawienia")
    user_kapital = st.number_input("Kapitał (PLN):", value=10000)
    wybrany_int = st.select_slider("Interwał:", options=list(interval_map.keys()), value="4 godz")
    tryb = st.radio("Cena wejścia:", ["Rynkowa", "Limit (EMA20)"])

st.title("⚖️ Skaner PRO V6.8 - Multi-Asset")
tab_k, tab_z = st.tabs(["₿ KRYPTOWALUTY", "🥇 SUROWCE, FOREX & INDEKSY"])

mode_key = "rynkowy" if tryb == "Rynkowa" else "limit"

with tab_k:
    dane_k = pobierz_krypto(wybrany_int)
    wyniki = []
    for s, df in dane_k.items():
        res = analizuj(df, user_kapital, mode_key)
        if res: wyniki.append({"Instrument": s, **res})
    if wyniki:
        st.dataframe(pd.DataFrame(wyniki).style.apply(stylizuj, axis=1), use_container_width=True)

with tab_z:
    dane_z = pobierz_zasoby(wybrany_int)
    wyniki_z = []
    for s, df in dane_z.items():
        res = analizuj(df, user_kapital, mode_key)
        if res: wyniki_z.append({"Instrument": s, **res})
    if wyniki_z:
        st.dataframe(pd.DataFrame(wyniki_z).style.apply(stylizuj, axis=1), use_container_width=True)
