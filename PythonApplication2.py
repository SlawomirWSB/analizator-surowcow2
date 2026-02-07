import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V9.2 - Heritage Colors", layout="wide")

# PEŁNA LISTA INSTRUMENTÓW XTB
KRYPTO_XTB = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "LINK": "LINK-USD",
    "MATIC": "MATIC-USD", "XRP": "XRP-USD", "ADA": "ADA-USD", "DOT": "DOT-USD",
    "LTC": "LTC-USD", "TRX": "TRX-USD", "DOGE": "DOGE-USD", "AVAX": "AVAX-USD",
    "AAVE": "AAVE-USD", "ALGO": "ALGO-USD", "APT": "APT-USD", "ATOM": "ATOM-USD",
    "BCH": "BCH-USD", "CHZ": "CHZ-USD", "FTM": "FTM-USD", "GRT": "GRT-USD", 
    "NEAR": "NEAR-USD", "OP": "OP-USD", "RNDR": "RNDR-USD", "UNI": "UNI-USD", 
    "XLM": "XLM-USD", "KAS": "KAS-USD", "STX": "STX-USD", "SHIB": "SHIB-USD"
}

ZASOBY_XTB = {
    "DAX 40": "^GDAXI", "Nasdaq 100": "^IXIC", "S&P 500": "^GSPC", "Dow Jones": "^DJI",
    "Złoto": "GC=F", "Srebro": "SI=F", "Ropa WTI": "CL=F", "Gaz": "NG=F", 
    "Miedź": "HG=F", "Kakao": "CC=F", "Kawa": "KC=F", "Cukier": "SB=F",
    "EUR/PLN": "EURPLN=X", "USD/PLN": "USDPLN=X", "EUR/USD": "EURUSD=X"
}

interval_map = {"5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

@st.cache_data(ttl=300)
def pobierz_dane(ticker_dict, int_label):
    tf = interval_map[int_label]
    data = {}
    for name, ticker in ticker_dict.items():
        try:
            df = yf.download(ticker, period="60d", interval=tf, progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                data[name] = df
        except: continue
    return data

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
        macd_h = float(l['MACDh_12_26_9'])
        v_rat = float(l['Volume'] / l['V_Avg']) if l['V_Avg'] > 0 else 1.0
        
        adx_min = 18 if ryzyko == "Poluzowany" else 25
        st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (35, 65)
        
        long = (c_akt > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0)
        short = (c_akt < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "KONSOLIDACJA" if adx < 15 else "CZEKAJ"
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl = wej - (atr * 1.5) if (sig == "KUP" or macd_h > 0) else wej + (atr * 1.5)
        tp = wej + (atr * 2.5) if (sig == "KUP" or macd_h > 0) else wej - (atr * 2.5)
        
        # Backtest
        td = df.tail(50).copy()
        td['E'] = ta.ema(td['Close'], length=20)
        cap, pos, tr = 1000.0, 0.0, 0
        for i in range(1, len(td)):
            px, ex = td['Close'].iloc[i], td['E'].iloc[i]
            if px > ex and pos == 0: pos, tr = cap / px, tr + 1
            elif px < ex and pos > 0: cap, pos = pos * px, 0.0; tr += 1
        res = cap if pos == 0 else pos * td['Close'].iloc[-1]
        hist = f"{round(((res-1000)/1000)*100, 1)}% ({tr})"

        return {
            "Instrument": name, "Sygnał": sig, "Siła %": (90 if sig in ["KUP", "SPRZEDAJ"] else 50),
            "Cena Rynkowa": round(c_akt, 4), "Cena Wejścia": round(wej, 4), "RSI": round(rsi, 1),
            "StochRSI": round(stoch, 1), "Pęd": "↑ Wzrost" if macd_h > 0 else "↓ Spadek",
            "ADX": round(adx, 1), "Wolumen %": round(v_rat * 100), "Ile (1%)": round((kapital*0.01)/abs(wej-sl), 4),
            "TP": round(tp, 4), "SL": round(sl, 4), "Hist. 50ś": hist
        }
    except: return None

# --- KLUCZOWE KOLOROWANIE Z WERSJI V8.3 ---
def stylizuj_heritage(row):
    s = [''] * len(row)
    idx = row.index.tolist()
    
    # Sygnał - Pełne tło (Styl V8.3)
    sig = row['Sygnał']
    if sig == 'KUP': 
        s[idx.index('Sygnał')] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': 
        s[idx.index('Sygnał')] = 'background-color: #ff0000; color: white; font-weight: bold'
    
    # Pęd i Wskaźniki - Kolor tekstu
    if "Wzrost" in row['Pęd']: s[idx.index('Pęd')] = 'color: #00ff00'
    else: s[idx.index('Pęd')] = 'color: #ff4b4b'
    
    # RSI / ADX / Stoch - wsparcie kolorem
    if row['ADX'] > 22: s[idx.index('ADX')] = 'color: #00ff00'
    if row['Wolumen %'] > 100: s[idx.index('Wolumen %')] = 'color: #00ff00'

    # Historia - Pełne ciemne tło (Styl V8.3)
    hist = row['Hist. 50ś']
    if "-" not in hist:
        s[idx.index('Hist. 50ś')] = 'background-color: #0e2f10; color: #00ff00; font-weight: bold'
    else:
        s[idx.index('Hist. 50ś')] = 'background-color: #2f0e0e; color: #ff4b4b; font-weight: bold'
    
    return s

# --- UI ---
with st.sidebar:
    st.header("⚙️ Konfiguracja")
    u_kapital = st.number_input("Kapitał (PLN):", value=10000)
    u_interwal = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    u_wejscie = st.radio("Metoda:", ["Rynkowa", "Limit (EMA20)"])
    u_ryzyko = st.radio("Ryzyko:", ["Poluzowany", "Rygorystyczny"])

st.title("⚖️ Skaner PRO V9.2 - Heritage Colors")

t1, t2 = st.tabs(["₿ KRYPTOWALUTY XTB", "📊 INDEKSY & TOWARY"])

for tab, tickers in zip([t1, t2], [KRYPTO_XTB, ZASOBY_XTB]):
    with tab:
        dane = pobierz_dane(tickers, u_interwal)
        wyniki = [analizuj(df, n, u_kapital, u_wejscie, u_ryzyko) for n, df in dane.items()]
        wyniki = [w for w in wyniki if w is not None]
        if wyniki:
            df_res = pd.DataFrame(wyniki).sort_values("Siła %", ascending=False)
            st.dataframe(df_res.style.apply(stylizuj_heritage, axis=1), use_container_width=True)
