import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V9.0 - XTB Native", layout="wide")

# PEŁNA LISTA KRYPTO (ZGODNIE Z XTB)
KRYPTO_XTB = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "LINK": "LINK-USD",
    "MATIC": "MATIC-USD", "XRP": "XRP-USD", "ADA": "ADA-USD", "DOT": "DOT-USD",
    "LTC": "LTC-USD", "TRX": "TRX-USD", "DOGE": "DOGE-USD", "AVAX": "AVAX-USD",
    "AAVE": "AAVE-USD", "ALGO": "ALGO-USD", "APT": "APT-USD", "ATOM": "ATOM-USD",
    "BCH": "BCH-USD", "CHZ": "CHZ-USD", "FTM": "FTM-USD", "GRT": "GRT-USD", 
    "NEAR": "NEAR-USD", "OP": "OP-USD", "RNDR": "RNDR-USD", "UNI": "UNI-USD", 
    "XLM": "XLM-USD", "KAS": "KAS-USD", "STX": "STX-USD", "SHIB": "SHIB-USD"
}

# PEŁNA LISTA INDEKSÓW I TOWARÓW
ZASOBY_XTB = {
    "US100 (Nasdaq)": "^IXIC", "DE40 (DAX)": "^GDAXI", "US500 (S&P)": "^GSPC",
    "US30 (Dow Jones)": "^DJI", "Złoto": "GC=F", "Srebro": "SI=F", "Ropa WTI": "CL=F",
    "Gaz": "NG=F", "Miedź": "HG=F", "Kukurydza": "ZC=F", "Pszenica": "ZW=F",
    "EUR/PLN": "EURPLN=X", "USD/PLN": "USDPLN=X", "EUR/USD": "EURUSD=X"
}

interval_map = {"5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

@st.cache_data(ttl=300)
def pobierz_dane(ticker_dict, int_label):
    tf = interval_map[int_label]
    data = {}
    for name, ticker in ticker_dict.items():
        try:
            df = yf.download(ticker, period="100d", interval=tf, progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                data[name] = df
        except: continue
    return data

def run_backtest(df):
    if len(df) < 50: return "0% (0)"
    td = df.tail(60).copy()
    td['EMA'] = ta.ema(td['Close'], length=20)
    cap, pos, trades = 1000.0, 0.0, 0
    for i in range(1, len(td)):
        p, e = td['Close'].iloc[i], td['EMA'].iloc[i]
        if p > e and pos == 0: pos, trades = cap / p, trades + 1
        elif p < e and pos > 0: cap, pos = pos * p, 0.0; trades += 1
    final = cap if pos == 0 else pos * td['Close'].iloc[-1]
    ret = round(((final - 1000) / 1000) * 100, 1)
    return f"{ret}% ({trades})"

def analizuj(df_raw, name, kapital, tryb, ryzyko):
    try:
        df = df_raw.copy()
        df.ta.rsi(append=True); df.ta.ema(length=20, append=True)
        df.ta.adx(append=True); df.ta.atr(append=True); df.ta.macd(append=True)
        df.ta.stochrsi(append=True)
        df['V_Avg'] = df['Volume'].rolling(20).mean()
        
        l = df.iloc[-1]
        c_akt, ema, atr = float(l['Close']), float(l['EMA_20']), float(l['ATRr_14'])
        adx, rsi, stoch = float(l['ADX_14']), float(l['RSI_14']), float(l['STOCHRSIk_14_14_3_3'])
        macd_h, v_rat = float(l['MACDh_12_26_9']), float(l['Volume'] / l['V_Avg']) if l['V_Avg'] > 0 else 1.0
        
        # PROGI
        adx_min = 18 if ryzyko == "Poluzowany" else 25
        st_buy, st_sell = (55, 45) if ryzyko == "Poluzowany" else (30, 70)
        
        long = (c_akt > ema) and (adx > adx_min) and (stoch < st_buy) and (macd_h > 0)
        short = (c_akt < ema) and (adx > adx_min) and (stoch > st_sell) and (macd_h < 0)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "KONSOLIDACJA" if adx < 15 else "CZEKAJ"
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl, tp = (wej - atr*1.5, wej + atr*2.5) if (macd_h > 0) else (wej + atr*1.5, wej - atr*2.5)
        
        return {
            "Instrument": name, "Sygnał": sig, "Siła %": (90 if sig in ["KUP", "SPRZEDAJ"] else 50),
            "Cena Rynkowa": round(c_akt, 4), "Cena Wejścia": round(wej, 4), "RSI": round(rsi, 1),
            "StochRSI": round(stoch, 1), "Pęd": "↑ Wzrost" if macd_h > 0 else "↓ Spadek",
            "ADX": round(adx, 1), "Wolumen %": round(v_rat * 100), "Ile (1%)": round((kapital*0.01)/abs(wej-sl), 4),
            "TP": round(tp, 4), "SL": round(sl, 4), "Hist. 50ś": run_backtest(df)
        }
    except: return None

def stylizuj(row, ryzyko):
    s = [''] * len(row)
    sig, ped, stoch = row['Sygnał'], row['Pęd'], row['StochRSI']
    st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (30, 70)
    
    if sig == 'KUP': s[1] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #ff0000; color: white; font-weight: bold'
    
    s[7] = 'color: #00ff00' if "Wzrost" in ped else 'color: #ff4b4b'
    if (sig == "KUP" and stoch < st_b) or (sig == "SPRZEDAJ" and stoch > st_s): s[6] = 'color: #00ff00; font-weight: bold'
    
    if "-" not in row['Hist. 50ś']: s[14] = 'background-color: #0e2f10; color: #00ff00'
    else: s[14] = 'background-color: #2f0e0e; color: #ff4b4b'
    return s

# --- UI ---
with st.sidebar:
    st.header("⚙️ Ustawienia")
    user_kap = st.number_input("Kapitał (PLN):", value=10000)
    int_val = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    metoda = st.radio("Wejście:", ["Rynkowa", "Limit (EMA20)"])
    ryzyko_val = st.radio("Ryzyko:", ["Poluzowany", "Rygorystyczny"])

st.title("⚖️ Skaner PRO V9.0 - XTB Native Stable")

t1, t2 = st.tabs(["₿ KRYPTO XTB", "📊 INDEKSY & TOWARY"])

for tab, tickers in zip([t1, t2], [KRYPTO_XTB, ZASOBY_XTB]):
    with tab:
        dane = pobierz_dane(tickers, int_val)
        wyniki = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in dane.items()]
        wyniki = [w for w in wyniki if w is not None]
        if wyniki:
            df_final = pd.DataFrame(wyniki).sort_values("Siła %", ascending=False)
            st.dataframe(df_final.style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)
