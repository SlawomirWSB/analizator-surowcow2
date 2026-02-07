import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import time
from concurrent.futures import ThreadPoolExecutor

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V8.8 - Ultra-Stable", layout="wide")

# Mapowanie tickerów krypto na format Yahoo (bezpieczniejszy przy dużej ilości)
KRYPTO_MAP = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "LINK": "LINK-USD",
    "MATIC": "MATIC-USD", "XRP": "XRP-USD", "ADA": "ADA-USD", "DOT": "DOT-USD",
    "LTC": "LTC-USD", "TRX": "TRX-USD", "DOGE": "DOGE-USD", "AVAX": "AVAX-USD",
    "AAVE": "AAVE-USD", "ALGO": "ALGO-USD", "APT": "APT-USD", "ATOM": "ATOM-USD",
    "BCH": "BCH-USD", "CHZ": "CHZ-USD", "DYDX": "DYDX-USD", "FTM": "FTM-USD",
    "GRT": "GRT-USD", "NEAR": "NEAR-USD", "OP": "OP-USD", "RNDR": "RNDR-USD",
    "UNI": "UNI-USD", "XLM": "XLM-USD", "KAS": "KAS-USD", "STX": "STX-USD"
}

ZASOBY_XTB = {
    "US100 (Nasdaq)": "^IXIC", "US30 (Dow Jones)": "^DJI", "US500 (S&P500)": "^GSPC",
    "DE40 (DAX)": "^GDAXI", "Złoto (GOLD)": "GC=F", "Srebro (SILVER)": "SI=F", 
    "Ropa WTI": "CL=F", "Gaz Naturalny": "NG=F", "EUR/USD": "EURUSD=X"
}

interval_map = {"5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

# --- SILNIK POBIERANIA (YFinance jest stabilniejszy dla wielu tickerów) ---
@st.cache_data(ttl=120, show_spinner=False)
def pobierz_dane_stabilne(ticker_dict, int_label):
    tf = interval_map[int_label]
    data = {}
    
    def fetch_data(name, ticker):
        try:
            # Krótszy okres dla szybszego ładowania
            df = yf.download(ticker, period="60d", interval=tf, progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                return name, df
        except: return name, None
        return name, None

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda x: fetch_data(x[0], x[1]), ticker_dict.items()))
    
    for name, df in results:
        if df is not None: data[name] = df
    return data

# --- ANALIZA ---
def run_backtest(df):
    if len(df) < 30: return "0% (0)"
    td = df.tail(50).copy()
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
        
        st_b, st_s, adx_min = (55, 45, 18) if ryzyko == "Poluzowany" else (30, 70, 25)
        
        long = (c_akt > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0)
        short = (c_akt < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "KONSOLIDACJA" if adx < 15 else "CZEKAJ"
        ped_icon = "↑ Wzrost" if macd_h > 0 else "↓ Spadek"
        
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl, tp = (wej - atr*1.5, wej + atr*2.5) if (sig == "KUP" or macd_h > 0) else (wej + atr*1.5, wej - atr*2.5)
        
        return {
            "Instrument": name, "Sygnał": sig, "Siła %": (90 if sig in ["KUP", "SPRZEDAJ"] else 50),
            "Cena Rynkowa": round(c_akt, 4), "Cena Wejścia": round(wej, 4), "RSI": round(rsi, 1),
            "StochRSI": round(stoch, 1), "Pęd": ped_icon, "ADX": round(adx, 1),
            "Wolumen %": round(v_rat * 100), "Ile (1%)": round((kapital*0.01)/abs(wej-sl), 4),
            "TP": round(tp, 4), "SL": round(sl, 4), "Hist. 50ś": run_backtest(df)
        }
    except: return None

def stylizuj(row, ryzyko):
    s = [''] * len(row)
    sig, ped, stoch = row['Sygnał'], row['Pęd'], row['StochRSI']
    st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (30, 70)
    
    if sig == 'KUP': s[1] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #ff0000; color: white; font-weight: bold'
    
    if "Wzrost" in ped: s[7] = 'color: #00ff00'
    else: s[7] = 'color: #ff4b4b'
    
    if (sig == "KUP" and stoch < st_b) or (sig == "SPRZEDAJ" and stoch > st_s):
        s[6] = 'color: #00ff00; font-weight: bold'
    return s

# --- GUI ---
with st.sidebar:
    st.header("⚙️ Konfiguracja V8.8")
    user_kap = st.number_input("Kapitał (PLN):", value=10000)
    int_val = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    metoda, ryzyko_val = st.radio("Wejście:", ["Rynkowa", "Limit (EMA20)"]), st.radio("Ryzyko:", ["Rygorystyczny", "Poluzowany"])

st.title("⚖️ Skaner PRO V8.8 - Ultra-Stable")
st.info("Przełączono na hybrydowe pobieranie danych. Jeśli jedna zakładka działa, druga również powinna się załadować.")

tab1, tab2 = st.tabs(["₿ KRYPTO XTB (Stabilne)", "📊 INDEKSY & TOWARY"])

with tab1:
    with st.spinner("Ładowanie krypto..."):
        d_k = pobierz_dane_stabilne(KRYPTO_MAP, int_val)
        if d_k:
            w_k = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in d_k.items() if analizuj(df, n, user_kap, metoda, ryzyko_val)]
            if w_k: st.dataframe(pd.DataFrame(w_k).sort_values("Siła %", ascending=False).style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)
        else: st.error("Błąd połączenia z serwerem krypto. Spróbuj zmienić interwał.")

with tab2:
    with st.spinner("Ładowanie indeksów..."):
        d_z = pobierz_dane_stabilne(ZASOBY_XTB, int_val)
        if d_z:
            w_z = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in d_z.items() if analizuj(df, n, user_kap, metoda, ryzyko_val)]
            if w_z: st.dataframe(pd.DataFrame(w_z).sort_values("Siła %", ascending=False).style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)
