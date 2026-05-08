import streamlit as st
import pandas as pd
import pandas_ta as ta
from tvdatafeed import TvDatafeed, Interval

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V9.7 - TV Engine", layout="wide")

# Nowe mapowanie (Symbol, Giełda) - Dane prosto z TV
KRYPTO_TV = {
    "BITCOIN": ("BTCUSDT", "BINANCE"), "ETHEREUM": ("ETHUSDT", "BINANCE"),
    "SOLANA": ("SOLUSDT", "BINANCE"), "CHAINLINK": ("LINKUSDT", "BINANCE"),
    "RIPPLE": ("XRPUSDT", "BINANCE"), "CARDANO": ("ADAUSDT", "BINANCE"),
    "DOT": ("DOTUSDT", "BINANCE"), "LITECOIN": ("LTCUSDT", "BINANCE"),
    "AVALANCHE": ("AVAXUSDT", "BINANCE"), "DOGECOIN": ("DOGEUSDT", "BINANCE")
}

ZASOBY_TV = {
    "GOLD": ("XAUUSD", "OANDA"), "SILVER": ("XAGUSD", "OANDA"),
    "OIL.WTI": ("WTIUSD", "OANDA"), "NATGAS": ("NATGASUSD", "OANDA"),
    "DE40 (DAX)": ("DE30EUR", "OANDA"), "US100 (NQ)": ("NAS100USD", "OANDA"),
    "US500 (SP)": ("SPX500USD", "OANDA"), "EURUSD": ("EURUSD", "FX_IDC"),
    "USDPLN": ("USDPLN", "OANDA"), "EURPLN": ("EURPLN", "OANDA")
}

interval_map = {
    "15 min": Interval.in_15_minute,
    "1 godz": Interval.in_1_hour,
    "4 godz": Interval.in_4_hour,
    "1 dzień": Interval.in_daily
}

@st.cache_resource # Używamy cache_resource dla połączenia TV
def get_tv_connection():
    return TvDatafeed()

def analizuj(df_raw, name, kapital, tryb, ryzyko):
    try:
        df = df_raw.copy()
        df.ta.rsi(append=True); df.ta.ema(length=20, append=True)
        df.ta.adx(append=True); df.ta.atr(append=True); df.ta.macd(append=True)
        df.ta.stochrsi(append=True)
        df['V_Avg'] = df['Volume'].rolling(20).mean()
        
        # Logika sygnału na zamkniętej świecy (iloc[-2])
        l = df.iloc[-2] 
        curr = df.iloc[-1]
        c_akt = float(curr['Close'])
        ema, atr = float(l['EMA_20']), float(l['ATRr_14'])
        adx, rsi, stoch = float(l['ADX_14']), float(l['RSI_14']), float(l['STOCHRSIk_14_14_3_3'])
        macd_h = float(l['MACDh_12_26_9'])
        v_rat = (float(l['Volume'] / l['V_Avg']) * 100) if l['V_Avg'] > 0 else 100.0
        
        adx_min = 18 if ryzyko == "Poluzowany" else 25
        st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (35, 65)
        
        long = (l['Close'] > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0)
        short = (l['Close'] < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "CZEKAJ"
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        sl = wej - (atr * 1.5) if sig == "KUP" else wej + (atr * 1.5)
        tp = wej + (atr * 2.5) if sig == "KUP" else wej - (atr * 2.5)
        
        return {
            "Instrument": name, "Sygnał": sig, "Siła %": (90 if sig in ["KUP", "SPRZEDAJ"] else 50),
            "Cena Rynkowa": round(c_akt, 4), "RSI": round(rsi, 1), "ADX": round(adx, 1),
            "Wolumen %": round(v_rat), "Ile (1%)": round((kapital*0.01)/abs(wej-sl), 4) if abs(wej-sl)>0 else 0,
            "TP": round(tp, 4), "SL": round(sl, 4)
        }
    except: return None

def stylizuj(row):
    s = [''] * len(row)
    idx = row.index.tolist()
    sig = row['Sygnał']
    if sig == 'KUP': s[idx.index('Sygnał')] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[idx.index('Sygnał')] = 'background-color: #ff0000; color: white; font-weight: bold'
    return s

# --- UI ---
st.title("⚖️ Skaner PRO V9.7 - Powered by TradingView Engine")
tv = get_tv_connection()

with st.sidebar:
    st.header("⚙️ Ustawienia")
    u_kap = st.number_input("Kapitał (PLN):", value=10000)
    u_int_label = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")
    u_wej = st.radio("Metoda:", ["Rynkowa", "Limit (EMA20)"])
    u_ryz = st.radio("Ryzyko:", ["Poluzowany", "Rygorystyczny"])

t1, t2 = st.tabs(["₿ KRYPTOWALUTY", "📊 INDEKSY & TOWARY"])

for tab, tickers in zip([t1, t2], [KRYPTO_TV, ZASOBY_TV]):
    with tab:
        wyniki = []
        for name, (symbol, exchange) in tickers.items():
            df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval_map[u_int_label], n_bars=100)
            if df is not None and not df.empty:
                df = df.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'})
                res = analizuj(df, name, u_kap, u_wej, u_ryz)
                if res: wyniki.append(res)
        
        if wyniki:
            df_res = pd.DataFrame(wyniki).sort_values("Siła %", ascending=False)
            st.dataframe(df_res.style.apply(stylizuj, axis=1), use_container_width=True)
