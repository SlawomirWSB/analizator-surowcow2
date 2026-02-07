import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V9.4 - XTB Ultra", layout="wide")

# MAKSYMALNA LISTA KRYPTO XTB (Wszystkie dostępne CFD)
KRYPTO_XTB = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "LINK": "LINK-USD",
    "MATIC": "MATIC-USD", "XRP": "XRP-USD", "ADA": "ADA-USD", "DOT": "DOT-USD",
    "LTC": "LTC-USD", "TRX": "TRX-USD", "DOGE": "DOGE-USD", "AVAX": "AVAX-USD",
    "AAVE": "AAVE-USD", "ALGO": "ALGO-USD", "APT": "APT-USD", "ATOM": "ATOM-USD",
    "BCH": "BCH-USD", "CHZ": "CHZ-USD", "FTM": "FTM-USD", "GRT": "GRT-USD", 
    "NEAR": "NEAR-USD", "OP": "OP-USD", "RNDR": "RNDR-USD", "UNI": "UNI-USD", 
    "XLM": "XLM-USD", "KAS": "KAS-USD", "STX": "STX-USD", "SHIB": "SHIB-USD",
    "EGLD": "EGLD-USD", "SAND": "SAND-USD", "MANA": "MANA-USD", "EOS": "EOS-USD",
    "FLOW": "FLOW-USD", "GALA": "GALA-USD", "HBAR": "HBAR-USD", "ICP": "ICP-USD",
    "IMX": "IMX-USD", "LDO": "LDO-USD", "MKR": "MKR-USD", "QNT": "QNT-USD",
    "VET": "VET-USD", "WAVES": "WAVES-USD", "ZEC": "ZEC-USD", "DYDX": "DYDX-USD",
    "CRV": "CRV-USD", "ENJ": "ENJ-USD", "LRC": "LRC-USD", "SNX": "SNX-USD", "BAT": "BAT-USD"
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
            if not df.empty and len(df) > 25:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                data[name] = df
        except: continue
    return data

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
        macd_h = float(l['MACDh_12_26_9'])
        v_rat = float(l['Volume'] / l['V_Avg']) * 100 if l['V_Avg'] > 0 else 100.0
        
        adx_min = 18 if ryzyko == "Poluzowany" else 25
        st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (35, 65)
        
        long = (c_akt > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0)
        short = (c_akt < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "CZEKAJ"
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl = wej - (atr * 1.5) if (macd_h > 0) else wej + (atr * 1.5)
        tp = wej + (atr * 2.5) if (macd_h > 0) else wej - (atr * 2.5)
        
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
            "StochRSI": round(stoch, 1), "Pęd": "Wzrost" if macd_h > 0 else "Spadek",
            "ADX": round(adx, 1), "Wolumen %": round(v_rat), "Ile (1%)": round((kapital*0.01)/abs(wej-sl), 4),
            "TP": round(tp, 4), "SL": round(sl, 4), "Hist. 50ś": hist
        }
    except: return None

def stylizuj_v9_4(row):
    s = [''] * len(row)
    idx = row.index.tolist()
    sig = row['Sygnał']
    
    # Sygnał
    if sig == 'KUP': s[idx.index('Sygnał')] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[idx.index('Sygnał')] = 'background-color: #ff0000; color: white; font-weight: bold'
    
    # Wolumen - NOWA LOGIKA
    vol = row['Wolumen %']
    if vol > 110: s[idx.index('Wolumen %')] = 'color: #00ff00; font-weight: bold' # Potwierdzenie
    elif vol < 60: s[idx.index('Wolumen %')] = 'color: #ff4b4b' # Słabość
    
    # Dynamika wskaźników
    s[idx.index('Pęd')] = 'color: #00ff00' if (sig == "KUP" and row['Pęd'] == "Wzrost") or (sig == "SPRZEDAJ" and row['Pęd'] == "Spadek") else 'color: #ff4b4b'
    s[idx.index('ADX')] = 'color: #00ff00' if row['ADX'] > 22 else 'color: #ff4b4b'
    
    # Historia
    if "-" not in row['Hist. 50ś']: s[idx.index('Hist. 50ś')] = 'background-color: #0e2f10; color: #00ff00'
    else: s[idx.index('Hist. 50ś')] = 'background-color: #2f0e0e; color: #ff4b4b'
    
    return s

# --- UI ---
with st.sidebar:
    st.header("⚙️ Konfiguracja V9.4")
    u_kap = st.number_input("Kapitał (PLN):", value=10000)
    u_int = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    u_wej = st.radio("Metoda:", ["Rynkowa", "Limit (EMA20)"])
    u_ryz = st.radio("Ryzyko:", ["Poluzowany", "Rygorystyczny"])

st.title("⚖️ Skaner PRO V9.4 - XTB Ultra Spectrum")

t1, t2 = st.tabs(["₿ KRYPTOWALUTY XTB", "📊 INDEKSY & TOWARY"])

for tab, tickers in zip([t1, t2], [KRYPTO_XTB, ZASOBY_XTB]):
    with tab:
        dane = pobierz_dane(tickers, u_int)
        wyniki = [analizuj(df, n, u_kap, u_wej, u_ryz) for n, df in dane.items()]
        wyniki = [w for w in wyniki if w is not None]
        if wyniki:
            df_res = pd.DataFrame(wyniki).sort_values("Siła %", ascending=False)
            st.dataframe(df_res.style.apply(stylizuj_v9_4, axis=1), use_container_width=True)
