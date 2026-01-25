import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner PRO - Analiza Wielowskaźnikowa", layout="wide")

KRYPTO_LISTA = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD"]

# POPRAWKA: Prawidłowe mapowanie interwałów
interval_map = {"1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}

def wykonaj_analize(symbol, interwal_label):
    interwal = interval_map[interwal_label]
    try:
        # Pobieramy nieco więcej danych, by wskaźniki (np. MACD) miały czas się "rozgrzać"
        df = yf.download(symbol, period="100d", interval=interwal, progress=False)
        if df.empty or len(df) < 50: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        # --- DODANIE NOWYCH WSKAŹNIKÓW ---
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.ema(length=50, append=True) # Dłuższa średnia dla trendu
        df.ta.atr(length=14, append=True)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        df.ta.adx(length=14, append=True) # Siła trendu
        df.ta.stoch(k=14, d=3, append=True) # Oscylator stochastyczny

        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        cena = float(last['Close'])
        rsi = float(last['RSI_14'])
        ema20 = float(last['EMA_20'])
        ema50 = float(last['EMA_50'])
        atr = float(last['ATRr_14'])
        adx = float(last['ADX_14'])
        macd = float(last['MACD_12_26_9'])
        macd_s = float(last['MACDs_12_26_9'])
        stoch_k = float(last['STOCHk_14_3_3'])

        # --- ZAAWANSOWANY SYSTEM PUNKTACJI (Scoring) ---
        score = 0
        
        # 1. Trend (EMA)
        if cena > ema20: score += 15
        if ema20 > ema50: score += 10 # Golden cross / trend wzrostowy
        
        # 2. Impuls (MACD)
        if macd > macd_s: score += 15
        if macd > 0: score += 5
        
        # 3. Wyprzedanie/Wykupienie (RSI + Stoch)
        if rsi < 30: score += 20 # Silne wyprzedanie
        elif rsi < 45: score += 10
        if stoch_k < 20: score += 10
        
        # 4. Siła trendu (ADX)
        if adx > 25: score += 10 # Trend jest silny, sygnał pewniejszy

        # Logika odwrotna dla sprzedaży
        sell_score = 0
        if cena < ema20: sell_score += 15
        if ema20 < ema50: sell_score += 10
        if macd < macd_s: sell_score += 15
        if rsi > 70: sell_score += 20
        if stoch_k > 80: sell_score += 10
        if adx > 25: sell_score += 10

        # Normalizacja do "Szansy %"
        total_buy = min(98, 30 + score)
        total_sell = min(98, 30 + sell_score)

        if total_buy > total_sell:
            sig, chance, oppo = "KUP", total_buy, total_sell
            tp, sl = cena + (atr * 2.5), cena - (atr * 1.5) # Zwiększony SL dla bezpieczeństwa
        else:
            sig, chance, oppo = "SPRZEDAJ", total_sell, total_buy
            tp, sl = cena - (atr * 2.5), cena + (atr * 1.5)

        return {
            "Instrument": symbol.replace("-USD", ""),
            "Sygnał": sig,
            "Siła Sygnału %": chance,
            "Trend (ADX)": round(adx, 1),
            "Cena": round(cena, 4),
            "TP": round(tp, 4),
            "SL": round(sl, 4),
            "RSI": round(rsi, 1),
            "ATR_HIDDEN": atr
        }
    except Exception as e:
        return None

# --- UI ---
st.title("⚖️ Skaner PRO - Analiza Wielowskaźnikowa")
interwal_sel = st.select_slider("Wybierz interwał analizy:", options=list(interval_map.keys()), value="4 godz")

if st.button("🚀 URUCHOM ANALIZĘ EKSPERCKĄ", use_container_width=True):
    wyniki = [res for s in KRYPTO_LISTA if (res := wykonaj_analize(s, interwal_sel))]
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Siła Sygnału %", ascending=False)
        
        def style_rows(row):
            color = '#1e4620' if row['Sygnał'] == 'KUP' else '#5f1a1d'
            return [f'background-color: {color}; color: white'] * len(row)

        st.dataframe(df_final.drop(columns=['ATR_HIDDEN']).style.apply(style_rows, axis=1), use_container_width=True)
        
        st.info("ADX > 25 oznacza silny trend. RSI < 30 lub > 70 sugeruje możliwe odwrócenie ceny.")
