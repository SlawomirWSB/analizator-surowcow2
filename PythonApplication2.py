import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V9.6 - XTB Native", layout="wide")

# MAPOWANIE: Nazwa wyświetlana (XTB) : Ticker Yahoo Finance
KRYPTO_XTB = {
    "BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD", "SOLANA": "SOL-USD", 
    "CHAINLINK": "LINK-USD", "POLYGON": "MATIC-USD", "RIPPLE": "XRP-USD", 
    "CARDANO": "ADA-USD", "DOT": "DOT-USD", "LITECOIN": "LTC-USD", 
    "TRON": "TRX-USD", "DOGECOIN": "DOGE-USD", "AVALANCHE": "AVAX-USD",
    "AAVE": "AAVE-USD", "ALGORAND": "ALGO-USD", "APTOS": "APT-USD", 
    "COSMOS": "ATOM-USD", "BITCOINCASH": "BCH-USD", "CHILIZ": "CHZ-USD", 
    "FANTOM": "FTM-USD", "THE_GRAPH": "GRT-USD", "NEAR": "NEAR-USD", 
    "OPTIMISM": "OP-USD", "RENDER": "RNDR-USD", "UNISWAP": "UNI-USD", 
    "STELLAR": "XLM-USD", "KASPA": "KAS-USD", "STACKS": "STX-USD", 
    "SHIBA_INU": "SHIB-USD", "ELROND": "EGLD-USD", "SANDBOX": "SAND-USD", 
    "DECENTRALAND": "MANA-USD", "EOS": "EOS-USD", "FLOW": "FLOW-USD", 
    "GALA": "GALA-USD", "HEDERA": "HBAR-USD", "INTERNET_COMP": "ICP-USD",
    "IMMUTABLE": "IMX-USD", "LIDO_DAO": "LDO-USD", "MAKER": "MKR-USD", 
    "QUANT": "QNT-USD", "VECHAIN": "VET-USD", "WAVES": "WAVES-USD", 
    "Z_CASH": "ZEC-USD", "DYDX": "DYDX-USD"
}

ZASOBY_XTB = {
    "DE40 (DAX)": "^GDAXI", "US100 (NQ)": "^IXIC", "US500 (SP)": "^GSPC",
    "GOLD": "GC=F", "SILVER": "SI=F", "OIL.WTI": "CL=F", "NATGAS": "NG=F", 
    "COPPER": "HG=F", "COCOA": "CC=F", "COFFEE": "KC=F", "SUGAR": "SB=F",
    "EURPLN": "EURPLN=X", "USDPLN": "USDPLN=X", "EURUSD": "EURUSD=X"
}

interval_map = {"5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

@st.cache_data(ttl=300)
def pobierz_dane(ticker_dict, int_label):
    tf = interval_map[int_label]
    data = {}
    for name, ticker in ticker_dict.items():
        try:
            df = yf.download(ticker, period="60d", interval=tf, progress=False)
            if not df.empty and len(df) > 20:
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
        v_rat = (float(l['Volume'] / l['V_Avg']) * 100) if l['V_Avg'] > 0 else 100.0
        
        adx_min = 18 if ryzyko == "Poluzowany" else 25
        st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (35, 65)
        
        long = (c_akt > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0)
        short = (c_akt < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "CZEKAJ"
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl = wej - (atr * 1.5) if (macd_h > 0) else wej + (atr * 1.5)
        tp = wej + (atr * 2.5) if (macd_h > 0) else wej - (atr * 2.5)
        
        # Historia (Backtest)
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

def stylizuj_v9_6(row):
    s = [''] * len(row)
    idx = row.index.tolist()
    sig = row['Sygnał']
    
    # 1. Kolorowanie Sygnału (Pełne tło)
    if sig == 'KUP': s[idx.index('Sygnał')] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[idx.index('Sygnał')] = 'background-color: #ff0000; color: white; font-weight: bold'
    
    # 2. Wskaźniki - Zielony jeśli wspierają trend
    def set_col(col_name, is_green):
        s[idx.index(col_name)] = 'color: #00ff00' if is_green else 'color: #ff4b4b'

    set_col('Pęd', (sig == "KUP" and row['Pęd'] == "Wzrost") or (sig == "SPRZEDAJ" and row['Pęd'] == "Spadek"))
    set_col('RSI', (sig == "KUP" and row['RSI'] < 65) or (sig == "SPRZEDAJ" and row['RSI'] > 35))
    set_col('StochRSI', (sig == "KUP" and row['StochRSI'] < 50) or (sig == "SPRZEDAJ" and row['StochRSI'] > 50))
    set_col('ADX', row['ADX'] > 20)
    
    # 3. Wolumen
    v = row['Wolumen %']
    s[idx.index('Wolumen %')] = 'color: #00ff00' if v > 105 else ('color: #ff4b4b' if v < 55 else '')

    # 4. Historia (Pełne tło)
    if "-" not in row['Hist. 50ś']: s[idx.index('Hist. 50ś')] = 'background-color: #0e2f10; color: #00ff00'
    else: s[idx.index('Hist. 50ś')] = 'background-color: #2f0e0e; color: #ff4b4b'
    
    return s

# --- UI ---
st.title("⚖️ Skaner PRO V9.6 - XTB Native Names")

with st.sidebar:
    st.header("⚙️ Ustawienia")
    u_kap = st.number_input("Kapitał (PLN):", value=10000)
    u_int = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    u_wej = st.radio("Metoda:", ["Rynkowa", "Limit (EMA20)"])
    u_ryz = st.radio("Ryzyko:", ["Poluzowany", "Rygorystyczny"])

t1, t2 = st.tabs(["₿ KRYPTOWALUTY (XTB NAMES)", "📊 INDEKSY & TOWARY"])

for tab, tickers in zip([t1, t2], [KRYPTO_XTB, ZASOBY_XTB]):
    with tab:
        dane = pobierz_dane(tickers, u_int)
        wyniki = [analizuj(df, n, u_kap, u_wej, u_ryz) for n, df in dane.items()]
        wyniki = [w for w in wyniki if w is not None]
        if wyniki:
            df_res = pd.DataFrame(wyniki).sort_values("Siła %", ascending=False)
            st.dataframe(df_res.style.apply(stylizuj_v9_6, axis=1), use_container_width=True)
