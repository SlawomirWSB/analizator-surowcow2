import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import yfinance as yf
import time

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V7.6 - Heatmap", layout="wide")

KRYPTO = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "LINK/USDT", "MATIC/USDT", "XRP/USDT", 
          "ADA/USDT", "DOT/USDT", "LTC/USDT", "TRX/USDT", "DOGE/USDT", "AVAX/USDT"]

ZASOBY = {
    "Złoto (GOLD)": "GC=F", "Srebro (SILVER)": "SI=F", "Ropa WTI (OIL)": "CL=F",
    "Miedź (COPPER)": "HG=F", "Gaz (NATGAS)": "NG=F", "Kakao (COCOA)": "CC=F",
    "EUR/PLN": "EURPLN=X", "USD/PLN": "USDPLN=X", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X",
    "S&P 500": "^GSPC", "DAX 40": "^GDAXI"
}

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1w", "1 mies": "1mo"
}

@st.cache_data(ttl=300)
def pobierz_krypto(int_label):
    ex = ccxt.binanceus()
    data = {}
    tf = interval_map[int_label]
    if tf == "1mo": tf = "1M"
    for sym in KRYPTO:
        try:
            ohlcv = ex.fetch_ohlcv(sym, timeframe=tf, limit=150)
            df = pd.DataFrame(ohlcv, columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            data[sym] = df.set_index(pd.to_datetime(df['time'], unit='ms'))
            time.sleep(0.01)
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
    td = df.tail(100).copy()
    td['EMA'] = ta.ema(td['Close'], length=20)
    cap, pos = 1000.0, 0.0
    for i in range(50, len(td)):
        p, e = td['Close'].iloc[i], td['EMA'].iloc[i]
        if p > e and pos == 0: pos = cap / p
        elif p < e and pos > 0: cap, pos = pos * p, 0.0
    final = cap if pos == 0 else pos * td['Close'].iloc[-1]
    return round(((final - 1000) / 1000) * 100, 2)

def analizuj(df_raw, kapital_pln, tryb_wejscia, stopien_ryzyka):
    try:
        df = df_raw.copy()
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.macd(append=True)
        df.ta.stochrsi(length=14, append=True)
        df['Vol_Avg'] = df['Volume'].rolling(20).mean()
        
        l = df.iloc[-1]
        cena_aktualna = float(l['Close'])
        ema20 = float(l['EMA_20'])
        a, r, atr = float(l['ADX_14']), float(l['RSI_14']), float(l['ATRr_14'])
        macd_h = float(l['MACDh_12_26_9'])
        stoch_k = float(l['STOCHRSIk_14_14_3_3'])
        vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1.0
        
        if stopien_ryzyka == "Rygorystyczny":
            stoch_buy, stoch_sell, adx_min, vol_min, buffer_mult = 30, 70, 25, 1.0, 0.15
        else:
            stoch_buy, stoch_sell, adx_min, vol_min, buffer_mult = 50, 50, 20, 0.8, 0.05
            
        buffer = atr * buffer_mult
        long_cond = (cena_aktualna > ema20 + buffer) and (a > adx_min) and (stoch_k < stoch_buy) and (macd_h > 0) and (vol_ratio >= vol_min)
        short_cond = (cena_aktualna < ema20 - buffer) and (a > adx_min) and (stoch_k > stoch_sell) and (macd_h < 0) and (vol_ratio >= vol_min)
        
        if long_cond: sig = "KUP"
        elif short_cond: sig = "SPRZEDAJ"
        elif a < 20: sig = "KONSOLIDACJA"
        else: sig = "CZEKAJ"
        
        wejscie = cena_aktualna if tryb_wejscia == "Rynkowa" else ema20
        sl_dist = atr * 1.5
        ilosc = (kapital_pln * 0.01) / sl_dist if sl_dist > 0 else 0
        
        return {
            "Instrument": "", "Sygnał": sig, "Siła %": min(98, 40 + (20 if a > 25 else 0) + (15 if vol_ratio > 1.1 else 0)),
            "Cena Rynkowa": round(cena_aktualna, 4), "Cena Wejścia": round(wejscie, 4),
            "RSI": round(r, 1), "StochRSI": round(stoch_k, 1), "Pęd": "Wzrost" if macd_h > 0 else "Spadek", 
            "ADX": round(a, 1), "Wolumen %": round(vol_ratio * 100), "Ile kupić (1%)": round(ilosc, 4),
            "TP": round(wejscie + (atr*2.5) if sig=="KUP" else wejscie - (atr*2.5), 4),
            "SL": round(wejscie - sl_dist if sig=="KUP" else wejscie + sl_dist, 4),
            "Hist. 50ś": f"{run_backtest(df)}%"
        }
    except: return None

# --- NOWA ZAAWANSOWANA STYLIZACJA ---
def stylizuj(row):
    s = [''] * len(row)
    sig = row['Sygnał']
    
    # Sygnał Główny
    if sig == 'KUP': s[1] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #ff0000; color: white; font-weight: bold'
    elif sig == 'KONSOLIDACJA': s[1] = 'background-color: #444444; color: #bbbbbb'
    
    # RSI (Kolorowanie pod kątem ekstremów)
    rsi = row['RSI']
    if rsi > 70: s[5] = 'background-color: #660000; color: white' # Przegrzanie
    elif rsi < 30: s[5] = 'background-color: #004400; color: white' # Wyprzedanie
    
    # StochRSI (Warunek wejścia)
    stoch = row['StochRSI']
    if stoch < 20: s[6] = 'color: #00ff00; border: 1px solid #00ff00'
    elif stoch > 80: s[6] = 'color: #ff4b4b; border: 1px solid #ff4b4b'
    
    # Pęd
    s[7] = 'color: #00ff00' if row['Pęd'] == 'Wzrost' else 'color: #ff4b4b'
    
    # ADX (Siła trendu)
    adx = row['ADX']
    if adx > 25: s[8] = 'background-color: #005500; color: white'
    elif adx < 20: s[8] = 'background-color: #333333; color: #ff9900'
    
    # Wolumen
    vol = row['Wolumen %']
    if vol > 120: s[9] = 'color: #00ff00; font-weight: bold'
    elif vol < 50: s[9] = 'color: #777777'

    # Historia
    v_h = float(row['Hist. 50ś'].replace('%',''))
    s[13] = 'background-color: #002200' if v_h > 5 else 'background-color: #220000' if v_h < -5 else ''
    
    return s

# --- INTERFEJS ---
with st.sidebar:
    st.header("⚙️ Ustawienia")
    user_kapital = st.number_input("Kapitał (PLN):", value=10000)
    wybrany_int = st.select_slider("Interwał:", options=list(interval_map.keys()), value="15 min")
    tryb = st.radio("Metoda wejścia:", ["Rynkowa", "Limit (EMA20)"])
    ryzyko = st.radio("Stopień Ryzyka:", ["Rygorystyczny", "Poluzowany"])

st.title("⚖️ Skaner PRO V7.6 - Heatmap Edition")

tab_k, tab_z = st.tabs(["₿ KRYPTOWALUTY", "🥇 SUROWCE & FOREX"])

for tab, data_func in zip([tab_k, tab_z], [pobierz_krypto, pobierz_zasoby]):
    with tab:
        dane = data_func(wybrany_int)
        wyniki = []
        if dane:
            for s, df in dane.items():
                res = analizuj(df, user_kapital, tryb, ryzyko)
                if res: 
                    res["Instrument"] = s
                    wyniki.append(res)
        
        if wyniki:
            df_final = pd.DataFrame(wyniki)[["Instrument", "Sygnał", "Siła %", "Cena Rynkowa", "Cena Wejścia", "RSI", "StochRSI", "Pęd", "ADX", "Wolumen %", "Ile kupić (1%)", "TP", "SL", "Hist. 50ś"]]
            st.dataframe(df_final.style.apply(stylizuj, axis=1), use_container_width=True)
