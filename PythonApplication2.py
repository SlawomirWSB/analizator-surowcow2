import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import yfinance as yf
import time

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V8.2 - Fixed Limits", layout="wide")

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

def analizuj(df_raw, name, kapital_pln, tryb_wejscia, stopien_ryzyka):
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
        
        # PROGI STRATEGII
        if stopien_ryzyka == "Rygorystyczny":
            stoch_buy_max, stoch_sell_min, adx_min, vol_min = 30, 70, 25, 1.0
        else:
            stoch_buy_max, stoch_sell_min, adx_min, vol_min = 50, 50, 20, 0.8
            
        long_cond = (cena_aktualna > ema20) and (a > adx_min) and (stoch_k < stoch_buy_max) and (macd_h > 0) and (vol_ratio >= vol_min)
        short_cond = (cena_aktualna < ema20) and (a > adx_min) and (stoch_k > stoch_sell_min) and (macd_h < 0) and (vol_ratio >= vol_min)
        
        if long_cond: sig = "KUP"
        elif short_cond: sig = "SPRZEDAJ"
        elif a < 20: sig = "KONSOLIDACJA"
        else: sig = "CZEKAJ"
        
        # --- POPRAWKA LIMITÓW ---
        wejscie = ema20 if tryb_wejscia == "Limit (EMA20)" else cena_aktualna
        sl_dist = atr * 1.5
        tp_dist = atr * 2.5

        if sig == "KUP" or (sig == "CZEKAJ" and macd_h > 0):
            sl = wejscie - sl_dist
            tp = wejscie + tp_dist
        elif sig == "SPRZEDAJ" or (sig == "CZEKAJ" and macd_h < 0):
            sl = wejscie + sl_dist
            tp = wejscie - tp_dist
        else:
            sl, tp = wejscie, wejscie

        # Ryzyko 1% kapitału (dystans od wejścia do SL)
        ryzyko_zl = kapital_pln * 0.01
        dystans_cenowy = abs(wejscie - sl)
        ilosc = ryzyko_zl / dystans_cenowy if dystans_cenowy > 0 else 0
        
        # Siła pod sortowanie
        sila = 40
        if sig in ["KUP", "SPRZEDAJ"]: sila = 85
        if a > 35: sila += 10

        return {
            "Instrument": name, "Sygnał": sig, "Siła %": min(98, sila),
            "Cena Rynkowa": round(cena_aktualna, 4), "Cena Wejścia": round(wejscie, 4),
            "RSI": round(r, 1), "StochRSI": round(stoch_k, 1), "Pęd": "Wzrost" if macd_h > 0 else "Spadek", 
            "ADX": round(a, 1), "Wolumen %": round(vol_ratio * 100), "Ile kupić (1%)": round(ilosc, 4),
            "TP": round(tp, 4), "SL": round(sl, 4), "Hist. 50ś": f"{run_backtest(df)}%"
        }
    except: return None

def stylizuj(row, stopien_ryzyka):
    s = [''] * len(row)
    sig, ped, stoch, adx, vol = row['Sygnał'], row['Pęd'], row['StochRSI'], row['ADX'], row['Wolumen %']
    
    stoch_buy_max = 50 if stopien_ryzyka == "Poluzowany" else 30
    stoch_sell_min = 50 if stopien_ryzyka == "Poluzowany" else 70
    adx_min = 20 if stopien_ryzyka == "Poluzowany" else 25

    if sig == 'KUP': s[1] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #ff0000; color: white; font-weight: bold'

    # LOGIKA KOLORÓW ZGODNA Z DECYZJĄ (ZIELONY = POTWIERDZENIE)
    if (sig == "KUP" and ped == "Wzrost") or (sig == "SPRZEDAJ" and ped == "Spadek"): s[7] = 'color: #00ff00'
    elif (sig == "KUP" and ped == "Spadek") or (sig == "SPRZEDAJ" and ped == "Wzrost"): s[7] = 'color: #ff4b4b'
    
    if sig == "KUP" or (sig == "CZEKAJ" and ped == "Wzrost"):
        s[6] = 'color: #00ff00' if stoch < stoch_buy_max else 'color: #ff4b4b'
    elif sig == "SPRZEDAJ" or (sig == "CZEKAJ" and ped == "Spadek"):
        s[6] = 'color: #00ff00' if stoch > stoch_sell_min else 'color: #ff4b4b'

    s[8] = 'color: #00ff00' if adx > adx_min else 'color: #ff4b4b'
    s[9] = 'color: #00ff00' if vol >= (80 if stopien_ryzyka == "Poluzowany" else 100) else 'color: #ff4b4b'

    return s

# --- INTERFEJS ---
with st.sidebar:
    st.header("⚙️ Ustawienia")
    user_kapital = st.number_input("Kapitał (PLN):", value=10000)
    wybrany_int = st.select_slider("Interwał:", options=list(interval_map.keys()), value="4 godz")
    tryb = st.radio("Metoda wejścia:", ["Rynkowa", "Limit (EMA20)"])
    ryzyko = st.radio("Stopień Ryzyka:", ["Rygorystyczny", "Poluzowany"])

st.title("⚖️ Skaner PRO V8.2 - Fixed Risk/Reward")
st.info(f"Poprawione limity dla pozycji 'Limit'. Zielony kolor = wskaźnik wspiera Twój scenariusz.")

tab_k, tab_z = st.tabs(["₿ KRYPTOWALUTY", "🥇 SUROWCE & FOREX"])

for tab, data_func in zip([tab_k, tab_z], [pobierz_krypto, pobierz_zasoby]):
    with tab:
        dane = data_func(wybrany_int)
        if dane:
            wyniki = [analizuj(df, name, user_kapital, tryb, ryzyko) for name, df in dane.items() if analizuj(df, name, user_kapital, tryb, ryzyko)]
            if wyniki:
                df_final = pd.DataFrame(wyniki).sort_values(by="Siła %", ascending=False)
                st.dataframe(df_final.style.apply(stylizuj, axis=1, stopien_ryzyka=ryzyko), use_container_width=True)
        else: st.warning("Pobieranie danych...")
