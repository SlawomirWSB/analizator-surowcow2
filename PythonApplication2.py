import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner Krypto PRO", layout="wide")

KRYPTO_LISTA = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "DOGE-USD", "AVAX-USD", "BCH-USD",
    "SHIB-USD", "ALGO-USD", "UNI-USD", "NEAR-USD", "ATOM-USD", "ICP-USD"
]

interval_map = {
    "1 min": "1m", "5 min": "5m", "15 min": "15m", "30 min": "30m",
    "1 godz": "1h", "4 godz": "1h", "1 dzień": "1d", "1 tydz": "1wk"
}

def wykonaj_analize(symbol, interwal_label):
    interwal = interval_map[interwal_label]
    okres_map = {"1m": "1d", "5m": "1d", "15m": "1d", "30m": "1d", "1h": "1mo", "1d": "2y"}
    
    try:
        df = yf.download(symbol, period=okres_map.get(interwal, "1mo"), interval=interwal, progress=False)
        if df.empty or len(df) < 30: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.atr(length=14, append=True)

        last = df.iloc[-1]
        cena = float(last['Close'])
        rsi = float(last['RSI_14'])
        atr = float(last['ATRr_14'])
        
        # Trend Wyższy (Daily)
        df_d = yf.download(symbol, period="60d", interval="1d", progress=False)
        if isinstance(df_d.columns, pd.MultiIndex): df_d.columns = df_d.columns.get_level_values(0)
        ema_d = ta.ema(df_d['Close'], length=20)
        trend_up = cena > float(ema_d.iloc[-1])

        # SCORING
        p_buy, p_sell = 40, 40
        if rsi < 30: p_buy += 25
        elif rsi > 70: p_sell += 25
        if cena > last['EMA_20']: p_buy += 15
        else: p_sell += 15
        if trend_up: p_buy += 15
        else: p_sell += 15

        # Werdykt
        if p_buy >= 60: sig, chance, oppo = "KUP", p_buy, p_sell
        elif p_sell >= 60: sig, chance, oppo = "SPRZEDAJ", p_sell, p_buy
        else: sig, chance, oppo = "CZEKAJ", max(p_buy, p_sell), min(p_buy, p_sell)

        # Obliczenia TP/SL dla głównego sygnału
        if sig == "KUP":
            tp, sl = cena + (atr * 2.5), cena - (atr * 1.2)
        else:
            tp, sl = cena - (atr * 2.5), cena + (atr * 1.2)

        return {
            "Instrument": symbol.replace("-USD", ""),
            "Sygnał": sig,
            "Szansa %": int(chance),
            "Opozycja %": int(oppo),
            "Cena": round(cena, 4),
            "Wejście": round(cena, 4),
            "TP": round(tp, 4),
            "SL": round(sl, 4),
            "RSI": round(rsi, 1),
            "ATR_VAL": atr
        }
    except: return None

# --- UI ---
st.title("⚖️ Skaner Kierunkowy PRO")
interwal_sel = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")

if st.button("🚀 ANALIZUJ RYNEK", use_container_width=True):
    wyniki = [res for s in KRYPTO_LISTA if (res := wykonaj_analize(s, interwal_sel))]
    
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        
        def style_rows(row):
            color = '#28a745' if row['Sygnał'] == 'KUP' else '#dc3545' if row['Sygnał'] == 'SPRZEDAJ' else ''
            return [f'background-color: {color}; color: white; font-weight: bold' if color else ''] * len(row)

        # Wyświetlanie tabeli z dopasowanymi kolumnami
        st.dataframe(
            df_final.drop(columns=['ATR_VAL']).style.apply(style_rows, axis=1), 
            use_container_width=True, 
            height=500
        )
        
        st.divider()
        # KALKULATOR POD SPODEM
        st.subheader("📋 Kalkulator Zleceń")
        c1, c2 = st.columns(2)
        with c1: sel_inst = st.selectbox("Instrument:", df_final['Instrument'])
        with c2: kier = st.radio("Kierunek:", ["KUPNO", "SPRZEDAŻ"], horizontal=True)
        
        d = df_final[df_final['Instrument'] == sel_inst].iloc[0]
        curr_cena, curr_atr = d['Cena'], d['ATR_VAL']
        
        res1, res2, res3 = st.columns(3)
        if kier == "KUPNO":
            res1.metric("Wejście", curr_cena)
            res2.metric("TP (Profit)", round(curr_cena + (curr_atr * 2.5), 4))
            res3.metric("SL (Stop)", round(curr_cena - (curr_atr * 1.2), 4))
        else:
            res1.metric("Wejście", curr_cena)
            res2.metric("TP (Profit)", round(curr_cena - (curr_atr * 2.5), 4))
            res3.metric("SL (Stop)", round(curr_cena + (curr_atr * 1.2), 4))
