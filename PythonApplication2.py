import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import yfinance as yf
import time

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V8.6 - XTB Full Fleet", layout="wide")

# ROZSZERZONA LISTA KRYPTO CFD (ZGODNIE Z OFERTĄ XTB)
KRYPTO_XTB = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "LINK/USDT", "MATIC/USDT", "XRP/USDT", 
    "ADA/USDT", "DOT/USDT", "LTC/USDT", "TRX/USDT", "DOGE/USDT", "AVAX/USDT",
    "AAVE/USDT", "ALGO/USDT", "APE/USDT", "APT/USDT", "ATOM/USDT", "AXS/USDT",
    "BCH/USDT", "CHZ/USDT", "CRV/USDT", "DYDX/USDT", "EGLD/USDT", "EOS/USDT",
    "FTM/USDT", "GALA/USDT", "GRT/USDT", "IMX/USDT", "MANA/USDT",
    "NEAR/USDT", "OP/USDT", "RNDR/USDT", "SAND/USDT", "SHIB/USDT", "STX/USDT",
    "THETA/USDT", "UNI/USDT", "VET/USDT", "XLM/USDT", "ZEC/USDT", "KAS/USDT"
]

# ROZSZERZONA LISTA INDEKSÓW I SUROWCÓW (ZGODNIE Z XTB)
ZASOBY_XTB = {
    "US100 (Nasdaq)": "^IXIC", "US30 (Dow Jones)": "^DJI", "US500 (S&P500)": "^GSPC",
    "DE40 (DAX)": "^GDAXI", "UK100 (FTSE)": "^FTSE", "HKComp": "^HSI",
    "Złoto (GOLD)": "GC=F", "Srebro (SILVER)": "SI=F", "Ropa WTI": "CL=F",
    "Gaz Naturalny": "NG=F", "Miedź": "HG=F", "Kawa": "KC=F", "Cukier": "SB=F",
    "EUR/PLN": "EURPLN=X", "USD/PLN": "USDPLN=X", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X"
}

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d"
}

@st.cache_data(ttl=180, show_spinner=False)
def pobierz_dane_krypto(int_label):
    ex = ccxt.binance({'enableRateLimit': True})
    data = {}
    tf = interval_map[int_label]
    prog_bar = st.progress(0)
    total = len(KRYPTO_XTB)
    
    for idx, sym in enumerate(KRYPTO_XTB):
        try:
            ohlcv = ex.fetch_ohlcv(sym, timeframe=tf, limit=100)
            df = pd.DataFrame(ohlcv, columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            data[sym] = df.set_index(pd.to_datetime(df['time'], unit='ms'))
        except: continue
        prog_bar.progress((idx + 1) / total)
    prog_bar.empty()
    return data

@st.cache_data(ttl=180, show_spinner=False)
def pobierz_dane_zasoby(int_label):
    data = {}
    tf = interval_map[int_label]
    for nazwa, ticker in ZASOBY_XTB.items():
        try:
            df = yf.download(ticker, period="1y", interval=tf, progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                data[nazwa] = df
        except: continue
    return data

def run_backtest(df):
    if len(df) < 50: return "0% (0)"
    td = df.tail(60).copy()
    td['EMA'] = ta.ema(td['Close'], length=20)
    cap, pos, trades = 1000.0, 0.0, 0
    for i in range(1, len(td)):
        p, e = td['Close'].iloc[i], td['EMA'].iloc[i]
        if p > e and pos == 0: 
            pos = cap / p
            trades += 1
        elif p < e and pos > 0: 
            cap, pos = pos * p, 0.0
            trades += 1
    final = cap if pos == 0 else pos * td['Close'].iloc[-1]
    ret = round(((final - 1000) / 1000) * 100, 1)
    return f"{ret}% ({trades})"

def analizuj(df_raw, name, kapital, tryb, ryzyko):
    try:
        df = df_raw.copy()
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.macd(append=True)
        df.ta.stochrsi(length=14, append=True)
        df['V_Avg'] = df['Volume'].rolling(20).mean()
        
        l = df.iloc[-1]
        c_akt, ema, atr = float(l['Close']), float(l['EMA_20']), float(l['ATRr_14'])
        adx, rsi, stoch = float(l['ADX_14']), float(l['RSI_14']), float(l['STOCHRSIk_14_14_3_3'])
        macd_h = float(l['MACDh_12_26_9'])
        v_rat = float(l['Volume'] / l['V_Avg']) if l['V_Avg'] > 0 else 1.0
        
        if ryzyko == "Rygorystyczny":
            st_b, st_s, adx_min, v_min = 25, 75, 25, 1.0
        else:
            st_b, st_s, adx_min, v_min = 55, 45, 18, 0.4
            
        long = (c_akt > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0) and (v_rat >= v_min)
        short = (c_akt < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0) and (v_rat >= v_min)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "KONSOLIDACJA" if adx < 15 else "CZEKAJ"
        
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl, tp = (wej - atr*1.5, wej + atr*2.5) if (sig == "KUP" or macd_h > 0) else (wej + atr*1.5, wej - atr*2.5)
        
        dist = abs(wej - sl)
        ilosc = (kapital * 0.01) / dist if dist > 0 else 0
        
        return {
            "Instrument": name, "Sygnał": sig, "Siła %": (90 if sig in ["KUP", "SPRZEDAJ"] else 50),
            "Cena Rynkowa": round(c_akt, 4), "Cena Wejścia": round(wej, 4),
            "RSI": round(rsi, 1), "StochRSI": round(stoch, 1), "Pęd": "Wzrost" if macd_h > 0 else "Spadek", 
            "ADX": round(adx, 1), "Wolumen %": round(v_rat * 100), "Ile kupić (1%)": round(ilosc, 4),
            "TP": round(tp, 4), "SL": round(sl, 4), "Hist. 60ś": run_backtest(df)
        }
    except: return None

def stylizuj(row, ryzyko):
    s = [''] * len(row)
    sig, ped, stoch, adx, vol, rsi = row['Sygnał'], row['Pęd'], row['StochRSI'], row['ADX'], row['Wolumen %'], row['RSI']
    st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (25, 75)
    
    if sig == 'KUP': s[1] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #ff0000; color: white; font-weight: bold'

    if sig == "KUP" or (sig == "CZEKAJ" and ped == "Wzrost"):
        s[5] = 'color: #00ff00' if rsi < 45 else ''
        s[6] = 'color: #00ff00' if stoch < st_b else 'color: #ff4b4b'
    elif sig == "SPRZEDAJ" or (sig == "CZEKAJ" and ped == "Spadek"):
        s[5] = 'color: #00ff00' if rsi > 55 else ''
        s[6] = 'color: #00ff00' if stoch > st_s else 'color: #ff4b4b'

    s[8] = 'color: #00ff00' if adx > (18 if ryzyko == "Poluzowany" else 25) else 'color: #ff4b4b'
    s[9] = 'color: #00ff00' if vol >= (40 if ryzyko == "Poluzowany" else 100) else 'color: #ff4b4b'
    return s

# --- GUI ---
with st.sidebar:
    st.header("⚙️ Konfiguracja")
    user_kap = st.number_input("Kapitał (PLN):", value=10000)
    int_val = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    metoda = st.radio("Wejście:", ["Rynkowa", "Limit (EMA20)"])
    ryzyko_val = st.radio("Ryzyko:", ["Rygorystyczny", "Poluzowany"])

st.title("⚖️ Skaner PRO V8.6 - XTB Full Fleet")
st.info("Dodano Indeksy (Nasdaq, DAX) oraz Towary. Optymalizacja pobierania dla 60+ instrumentów.")

tab1, tab2 = st.tabs(["₿ KRYPTO CFD", "📊 INDEKSY, TOWARY, FX"])

with tab1:
    with st.spinner("Pobieranie krypto..."):
        d_k = pobierz_dane_krypto(int_val)
        if d_k:
            w_k = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in d_k.items() if analizuj(df, n, user_kap, metoda, ryzyko_val)]
            if w_k:
                df_k = pd.DataFrame(w_k).sort_values("Siła %", ascending=False)
                st.dataframe(df_k.style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)

with tab2:
    with st.spinner("Pobieranie indeksów i surowców..."):
        d_z = pobierz_dane_zasoby(int_val)
        if d_z:
            w_z = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in d_z.items() if analizuj(df, n, user_kap, metoda, ryzyko_val)]
            if w_z:
                df_z = pd.DataFrame(w_z).sort_values("Siła %", ascending=False)
                st.dataframe(df_z.style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)
