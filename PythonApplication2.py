import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner PRO - Precyzja", layout="wide")

KRYPTO_LISTA = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD"]

interval_map = {"1 godz": "1h", "4 godz": "1h", "1 dzień": "1d"}

def wykonaj_analize(symbol, interwal_label):
    interwal = interval_map[interwal_label]
    try:
        df = yf.download(symbol, period="60d", interval=interwal, progress=False)
        if df.empty or len(df) < 35: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        # Wskaźniki
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.atr(length=14, append=True)
        
        last = df.iloc[-1]
        cena = float(last['Close'])
        rsi = float(last['RSI_14'])
        ema = float(last['EMA_20'])
        atr = float(last['ATRr_14'])

        # 1. PŁYNNA PUNKTACJA (Zamiast sztywnych 70%, liczymy precyzyjnie)
        # Szansa KUPNA
        p_buy = 0
        p_buy += max(0, (50 - rsi) * 1.2) # Im niższe RSI, tym więcej punktów
        if cena > ema: p_buy += 20
        else: p_buy -= 10
        
        # Szansa SPRZEDAŻY
        p_sell = 0
        p_sell += max(0, (rsi - 50) * 1.2) # Im wyższe RSI, tym więcej punktów
        if cena < ema: p_sell += 20
        else: p_sell -= 10

        # Wynik końcowy (normalizacja do bazy 50 pkt)
        total_buy = int(40 + p_buy)
        total_sell = int(40 + p_sell)

        if total_buy > total_sell:
            sig, chance, oppo = "KUP", total_buy, total_sell
            tp, sl = cena + (atr * 2.5), cena - (atr * 1.2)
        else:
            sig, chance, oppo = "SPRZEDAJ", total_sell, total_buy
            tp, sl = cena - (atr * 2.5), cena + (atr * 1.2)

        return {
            "Instrument": symbol.replace("-USD", ""),
            "Sygnał": sig,
            "Szansa %": min(95, chance),
            "Opozycja %": min(95, oppo),
            "Cena": round(cena, 4),
            "Wejście": round(cena, 4),
            "TP": round(tp, 4),
            "SL": round(sl, 4),
            "RSI": round(rsi, 1),
            "ATR_HIDDEN": atr
        }
    except: return None

# --- UI ---
st.title("⚖️ Skaner PRO - Analiza Precyzyjna")
interwal_sel = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="1 godz")

if st.button("🚀 URUCHOM ANALIZĘ", use_container_width=True):
    wyniki = [res for s in KRYPTO_LISTA if (res := wykonaj_analize(s, interwal_sel))]
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        
        # Stylizacja
        def style_rows(row):
            color = '#1e4620' if row['Sygnał'] == 'KUP' else '#5f1a1d'
            return [f'background-color: {color}; color: white'] * len(row)

        # Wyświetlanie tabeli (Szerokość dopasowana automatycznie)
        st.dataframe(df_final.drop(columns=['ATR_HIDDEN']).style.apply(style_rows, axis=1), use_container_width=True)
        
        # KALKULATOR
        st.divider()
        st.subheader("📋 Szybki Kalkulator Zleceń")
        c1, c2, c3 = st.columns([1,1,2])
        with c1: inst = st.selectbox("Moneta:", df_final['Instrument'])
        with c2: kier = st.radio("Kierunek:", ["KUPNO", "SPRZEDAŻ"])
        
        d = df_final[df_final['Instrument'] == inst].iloc[0]
        curr_c, curr_a = d['Cena'], d['ATR_HIDDEN']
        
        with c3:
            if kier == "KUPNO":
                st.success(f"WEJŚCIE: {curr_c} | TP: {round(curr_c + (curr_a*2.5),4)} | SL: {round(curr_c - (curr_a*1.2),4)}")
            else:
                st.error(f"WEJŚCIE: {curr_c} | TP: {round(curr_c - (curr_a*2.5),4)} | SL: {round(curr_c + (curr_a*1.2),4)}")
