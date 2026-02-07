import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import yfinance as yf
import time
from concurrent.futures import ThreadPoolExecutor

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V8.7 - Turbo Parallel", layout="wide")

KRYPTO_XTB = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "LINK/USDT", "MATIC/USDT", "XRP/USDT", 
    "ADA/USDT", "DOT/USDT", "LTC/USDT", "TRX/USDT", "DOGE/USDT", "AVAX/USDT",
    "AAVE/USDT", "ALGO/USDT", "APE/USDT", "APT/USDT", "ATOM/USDT", "AXS/USDT",
    "BCH/USDT", "CHZ/USDT", "CRV/USDT", "DYDX/USDT", "EGLD/USDT", "EOS/USDT",
    "FTM/USDT", "GALA/USDT", "GRT/USDT", "IMX/USDT", "MANA/USDT",
    "NEAR/USDT", "OP/USDT", "RNDR/USDT", "SAND/USDT", "SHIB/USDT", "STX/USDT",
    "THETA/USDT", "UNI/USDT", "VET/USDT", "XLM/USDT", "ZEC/USDT", "KAS/USDT"
]

ZASOBY_XTB = {
    "US100 (Nasdaq)": "^IXIC", "US30 (Dow Jones)": "^DJI", "US500 (S&P500)": "^GSPC",
    "DE40 (DAX)": "^GDAXI", "UK100 (FTSE)": "^FTSE", "Złoto (GOLD)": "GC=F", 
    "Srebro (SILVER)": "SI=F", "Ropa WTI": "CL=F", "Gaz Naturalny": "NG=F", 
    "EUR/PLN": "EURPLN=X", "USD/PLN": "USDPLN=X", "EUR/USD": "EURUSD=X"
}

interval_map = {"5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

# --- SILNIK POBIERANIA (RÓWNOLEGŁY) ---
def fetch_single_crypto(ex, sym, tf):
    try:
        ohlcv = ex.fetch_ohlcv(sym, timeframe=tf, limit=100)
        df = pd.DataFrame(ohlcv, columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        return sym, df.set_index(pd.to_datetime(df['time'], unit='ms'))
    except: return sym, None

@st.cache_data(ttl=120, show_spinner=False)
def pobierz_dane_turbo(int_label):
    ex = ccxt.binance({'enableRateLimit': True})
    tf = interval_map[int_label]
    data = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda s: fetch_single_crypto(ex, s, tf), KRYPTO_XTB))
    for sym, df in results:
        if df is not None: data[sym] = df
    return data

@st.cache_data(ttl=120, show_spinner=False)
def pobierz_zasoby_turbo(int_label):
    tf = interval_map[int_label]
    data = {}
    def fetch_yf(name, ticker):
        try:
            df = yf.download(ticker, period="1y", interval=tf, progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                return name, df
        except: return name, None
        return name, None

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda x: fetch_yf(x[0], x[1]), ZASOBY_XTB.items()))
    for name, df in results:
        if df is not None: data[name] = df
    return data

# --- ANALIZA (LOGIKA V8.4 ADAPTIVE) ---
def run_backtest(df):
    if len(df) < 50: return "0% (0)"
    td = df.tail(60).copy()
    td['EMA'] = ta.ema(td['Close'], length=20)
    cap, pos, trades = 1000.0, 0.0, 0
    for i in range(1, len(td)):
        p, e = td['Close'].iloc[i], td['EMA'].iloc[i]
        if p > e and pos == 0: pos, trades = cap / p, trades + 1
        elif p < e and pos > 0: cap, pos, trades = pos * p, 0.0, trades + 1
    final = cap if pos == 0 else pos * td['Close'].iloc[-1]
    return f"{round(((final - 1000) / 1000) * 100, 1)}% ({trades})"

def analizuj(df_raw, name, kapital, tryb, ryzyko):
    try:
        df = df_raw.copy()
        df.ta.rsi(length=14, append=True); df.ta.ema(length=20, append=True)
        df.ta.adx(length=14, append=True); df.ta.atr(length=14, append=True)
        df.ta.macd(append=True); df.ta.stochrsi(length=14, append=True)
        df['V_Avg'] = df['Volume'].rolling(20).mean()
        
        l = df.iloc[-1]
        c_akt, ema, atr = float(l['Close']), float(l['EMA_20']), float(l['ATRr_14'])
        adx, rsi, stoch = float(l['ADX_14']), float(l['RSI_14']), float(l['STOCHRSIk_14_14_3_3'])
        macd_h, v_rat = float(l['MACDh_12_26_9']), float(l['Volume'] / l['V_Avg']) if l['V_Avg'] > 0 else 1.0
        
        st_b, st_s, adx_min, v_min = (55, 45, 18, 0.4) if ryzyko == "Poluzowany" else (25, 75, 25, 1.0)
        
        long = (c_akt > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0) and (v_rat >= v_min)
        short = (c_akt < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0) and (v_rat >= v_min)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "KONSOLIDACJA" if adx < 15 else "CZEKAJ"
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl, tp = (wej - atr*1.5, wej + atr*2.5) if (sig == "KUP" or macd_h > 0) else (wej + atr*1.5, wej - atr*2.5)
        
        return {
            "Instrument": name, "Sygnał": sig, "Siła %": (90 if sig in ["KUP", "SPRZEDAJ"] else 50),
            "Cena Rynkowa": round(c_akt, 4), "Cena Wejścia": round(wej, 4), "RSI": round(rsi, 1),
            "StochRSI": round(stoch, 1), "Pęd": "Wzrost" if macd_h > 0 else "Spadek", "ADX": round(adx, 1),
            "Wolumen %": round(v_rat * 100), "Ile kupić (1%)": round((kapital*0.01)/abs(wej-sl), 4),
            "TP": round(tp, 4), "SL": round(sl, 4), "Hist. 60ś": run_backtest(df)
        }
    except: return None

def stylizuj(row, ryzyko):
    s = [''] * len(row)
    sig, ped, stoch, adx, vol, rsi = row['Sygnał'], row['Pęd'], row['StochRSI'], row['ADX'], row['Wolumen %'], row['RSI']
    st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (30, 70)
    if sig == 'KUP': s[1] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #ff0000; color: white; font-weight: bold'
    if sig == "KUP" or (sig == "CZEKAJ" and ped == "Wzrost"):
        if rsi < 45: s[5] = 'color: #00ff00'
        s[6] = 'color: #00ff00' if stoch < st_b else 'color: #ff4b4b'
    elif sig == "SPRZEDAJ" or (sig == "CZEKAJ" and ped == "Spadek"):
        if rsi > 55: s[5] = 'color: #00ff00'
        s[6] = 'color: #00ff00' if stoch > st_s else 'color: #ff4b4b'
    s[8] = 'color: #00ff00' if adx > (18 if ryzyko == "Poluzowany" else 25) else 'color: #ff4b4b'
    s[9] = 'color: #00ff00' if vol >= (40 if ryzyko == "Poluzowany" else 100) else 'color: #ff4b4b'
    return s

# --- GUI ---
with st.sidebar:
    st.header("⚙️ Ustawienia")
    user_kap = st.number_input("Kapitał (PLN):", value=10000)
    int_val = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    metoda, ryzyko_val = st.radio("Wejście:", ["Rynkowa", "Limit (EMA20)"]), st.radio("Ryzyko:", ["Rygorystyczny", "Poluzowany"])

st.title("⚖️ Skaner PRO V8.7 - Turbo Parallel")
tab1, tab2 = st.tabs(["₿ KRYPTO CFD (41)", "📊 INDEKSY & TOWARY"])

with tab1:
    with st.spinner("Pobieranie równoległe krypto..."):
        d_k = pobierz_dane_turbo(int_val)
        w_k = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in d_k.items() if analizuj(df, n, user_kap, metoda, ryzyko_val)]
        if w_k: st.dataframe(pd.DataFrame(w_k).sort_values("Siła %", ascending=False).style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)

with tab2:
    with st.spinner("Pobieranie indeksów..."):
        d_z = pobierz_zasoby_turbo(int_val)
        w_z = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in d_z.items() if analizuj(df, n, user_kap, metoda, ryzyko_val)]
        if w_z: st.dataframe(pd.DataFrame(w_z).sort_values("Siła %", ascending=False).style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)
