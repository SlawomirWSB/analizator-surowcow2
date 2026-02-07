import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import time
from concurrent.futures import ThreadPoolExecutor

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V8.9 - XTB Heritage", layout="wide")

# PEŁNA LISTA KRYPTOWALUT CFD DOSTĘPNYCH NA XTB (Mapowanie Yahoo dla stabilności)
KRYPTO_XTB = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "LINK": "LINK-USD",
    "MATIC": "MATIC-USD", "XRP": "XRP-USD", "ADA": "ADA-USD", "DOT": "DOT-USD",
    "LTC": "LTC-USD", "TRX": "TRX-USD", "DOGE": "DOGE-USD", "AVAX": "AVAX-USD",
    "AAVE": "AAVE-USD", "ALGO": "ALGO-USD", "APT": "APT-USD", "ATOM": "ATOM-USD",
    "BCH": "BCH-USD", "CHZ": "CHZ-USD", "DYDX": "DYDX-USD", "FTM": "FTM-USD",
    "GRT": "GRT-USD", "NEAR": "NEAR-USD", "OP": "OP-USD", "RNDR": "RNDR-USD",
    "UNI": "UNI-USD", "XLM": "XLM-USD", "KAS": "KAS-USD", "STX": "STX-USD",
    "SHIB": "SHIB-USD", "SAND": "SAND-USD", "MANA": "MANA-USD", "EOS": "EOS-USD"
}

# PEŁNA LISTA INDEKSÓW I TOWARÓW XTB
ZASOBY_XTB = {
    "DAX 40 (DE40)": "^GDAXI", "Nasdaq 100 (US100)": "^IXIC", "S&P 500 (US500)": "^GSPC",
    "Dow Jones (US30)": "^DJI", "Złoto (GOLD)": "GC=F", "Srebro (SILVER)": "SI=F",
    "Ropa WTI (OIL)": "CL=F", "Gaz (NATGAS)": "NG=F", "Miedź (COPPER)": "HG=F",
    "Kakao (COCOA)": "CC=F", "Kawa (COFFEE)": "KC=F", "Cukier (SUGAR)": "SB=F",
    "EUR/PLN": "EURPLN=X", "USD/PLN": "USDPLN=X", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X"
}

interval_map = {"5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

# --- SILNIK POBIERANIA ---
@st.cache_data(ttl=120, show_spinner=False)
def pobierz_batch(ticker_dict, int_label):
    tf = interval_map[int_label]
    data = {}
    def fetch(name, ticker):
        try:
            df = yf.download(ticker, period="100d", interval=tf, progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                return name, df
        except: return name, None
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda x: fetch(x[0], x[1]), ticker_dict.items()))
    for name, df in results:
        if df is not None: data[name] = df
    return data

# --- ANALIZA V8.3 (Zwiększona liczba sygnałów) ---
def analizuj(df_raw, name, kapital, tryb, ryzyko):
    try:
        df = df_raw.copy()
        df.ta.rsi(length=14, append=True); df.ta.ema(length=20, append=True)
        df.ta.adx(length=14, append=True); df.ta.atr(length=14, append=True)
        df.ta.macd(append=True); df.ta.stochrsi(length=14, append=True)
        df['Vol_Avg'] = df['Volume'].rolling(20).mean()
        
        l = df.iloc[-1]
        c_akt, ema, atr = float(l['Close']), float(l['EMA_20']), float(l['ATRr_14'])
        adx, rsi, stoch = float(l['ADX_14']), float(l['RSI_14']), float(l['STOCHRSIk_14_14_3_3'])
        macd_h, v_rat = float(l['MACDh_12_26_9']), float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1.0
        
        # PARAMETRY ADAPTACYJNE (Więcej sygnałów)
        if ryzyko == "Poluzowany":
            st_b, st_s, adx_min, vol_min = 55, 45, 18, 0.5
        else:
            st_b, st_s, adx_min, vol_min = 35, 65, 22, 0.8
            
        long = (c_akt > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0)
        short = (c_akt < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "KONSOLIDACJA" if adx < 15 else "CZEKAJ"
        
        # LOGIKA V8.4 (Backtest z liczbą transakcji)
        td = df.tail(60).copy()
        td['E'] = ta.ema(td['Close'], length=20)
        c, p, t = 1000.0, 0.0, 0
        for i in range(1, len(td)):
            px, ex = td['Close'].iloc[i], td['E'].iloc[i]
            if px > ex and p == 0: p, t = c / px, t + 1
            elif px < ex and p > 0: c, p, t = p * px, 0.0, t + 1
        hist_ret = f"{round((( (c if p==0 else p*td['Close'].iloc[-1]) - 1000)/1000)*100,1)}% ({t})"

        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl, tp = (wej - atr*1.5, wej + atr*2.5) if (sig == "KUP" or macd_h > 0) else (wej + atr*1.5, wej - atr*2.5)
        
        return {
            "Instrument": name, "Sygnał": sig, "Siła %": (90 if sig in ["KUP", "SPRZEDAJ"] else 60 if adx > 20 else 40),
            "Cena Rynkowa": round(c_akt, 4), "Cena Wejścia": round(wej, 4), "RSI": round(rsi, 1),
            "StochRSI": round(stoch, 1), "Pęd": "↑ Wzrost" if macd_h > 0 else "↓ Spadek", "ADX": round(adx, 1),
            "Wolumen %": round(v_rat * 100), "Ile kupić (1%)": round((kapital*0.01)/abs(wej-sl), 4),
            "TP": round(tp, 4), "SL": round(sl, 4), "Hist. 50ś": hist_ret
        }
    except: return None

def stylizuj(row, ryzyko):
    s = [''] * len(row)
    sig, ped, stoch, adx, vol = row['Sygnał'], row['Pęd'], row['StochRSI'], row['ADX'], row['Wolumen %']
    st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (35, 65)
    
    if sig == 'KUP': s[1] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #ff0000; color: white; font-weight: bold'
    
    s[7] = 'color: #00ff00' if "Wzrost" in ped else 'color: #ff4b4b'
    if (sig == "KUP" and stoch < st_b) or (sig == "SPRZEDAJ" and stoch > st_s): s[6] = 'color: #00ff00'
    s[8] = 'color: #00ff00' if adx > 22 else 'color: #ff4b4b'
    s[9] = 'color: #00ff00' if vol > 100 else ''
    
    # Kolorowanie historii (z V8.4)
    if "-" not in row['Hist. 50ś']: s[14] = 'background-color: #0e2f10; color: #00ff00'
    else: s[14] = 'background-color: #2f0e0e; color: #ff4b4b'
    
    return s

# --- GUI ---
with st.sidebar:
    st.header("⚙️ Ustawienia XTB")
    user_kap = st.number_input("Kapitał (PLN):", value=10000)
    int_val = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    metoda = st.radio("Metoda wejścia:", ["Rynkowa", "Limit (EMA20)"])
    ryzyko_val = st.radio("Stopień Ryzyka:", ["Poluzowany", "Rygorystyczny"])

st.title("⚖️ Skaner PRO V8.9 - XTB Heritage Edition")

tab1, tab2 = st.tabs(["₿ KRYPTOWALUTY (XTB)", "📊 INDEKSY & SUROWCE"])

with tab1:
    d_k = pobierz_batch(KRYPTO_XTB, int_val)
    if d_k:
        w_k = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in d_k.items() if analizuj(df, n, user_kap, metoda, ryzyko_val)]
        if w_k:
            df_k = pd.DataFrame(w_k).sort_values("Siła %", ascending=False)
            st.dataframe(df_k.style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)

with tab2:
    d_z = pobierz_batch(ZASOBY_XTB, int_val)
    if d_z:
        w_z = [analizuj(df, n, user_kap, metoda, ryzyko_val) for n, df in d_z.items() if analizuj(df, n, user_kap, metoda, ryzyko_val)]
        if w_z:
            df_z = pd.DataFrame(w_z).sort_values("Siła %", ascending=False)
            st.dataframe(df_z.style.apply(stylizuj, axis=1, ryzyko=ryzyko_val), use_container_width=True)
