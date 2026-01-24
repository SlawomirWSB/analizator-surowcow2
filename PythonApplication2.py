import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner Krypto LOGIC", layout="wide")

KRYPTO_LISTA = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "DOGE-USD", "AVAX-USD", "BCH-USD",
    "SHIB-USD", "ALGO-USD", "UNI-USD", "NEAR-USD", "ATOM-USD", "ICP-USD", 
    "XLM-USD", "ETC-USD", "FIL-USD", "SAND-USD", "MANA-USD", "AAVE-USD"
]

interval_map = {
    "1 min": "1m", "5 min": "5m", "15 min": "15m", "30 min": "30m",
    "1 godz": "1h", "4 godz": "1h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

def pobierz_dane(symbol, interwal, okres):
    try:
        df = yf.download(symbol, period=okres, interval=interwal, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return pd.DataFrame()

def wykonaj_analize(symbol, interwal_label):
    interwal = interval_map[interwal_label]
    okres_map = {"1m": "1d", "5m": "1d", "15m": "1d", "30m": "1d", "1h": "1mo", "1d": "2y", "1wk": "max", "1mo": "max"}
    
    df = pobierz_dane(symbol, interwal, okres_map.get(interwal, "2y"))
    if df.empty or len(df) < 50: return None

    df.ta.rsi(length=14, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=50, append=True)
    df.ta.atr(length=14, append=True)

    last = df.iloc[-1]
    cena = float(last['Close'])
    rsi = float(last['RSI_14'])
    atr = float(last['ATRr_14'])
    
    # FILTR TRENDU WYŻSZEGO
    tf_wyzszy = "1d" if "m" in interwal or "h" in interwal else "1wk"
    df_big = pobierz_dane(symbol, tf_wyzszy, "2y")
    trend_wyzszy_ok = True
    if not df_big.empty and len(df_big) > 20:
        ema_big = ta.ema(df_big['Close'], length=20)
        trend_wyzszy_ok = float(df_big['Close'].iloc[-1]) > float(ema_big.iloc[-1])

    # --- NOWA LOGIKA SYGNAŁÓW (NIEZALEŻNA) ---
    # Punkty dla KUPNA
    p_buy = 50
    if rsi < 35: p_buy += 15
    if cena > last['EMA_20']: p_buy += 10
    if trend_wyzszy_ok: p_buy += 25
    else: p_buy -= 20

    # Punkty dla SPRZEDAŻY
    p_sell = 50
    if rsi > 65: p_sell += 15
    if cena < last['EMA_20']: p_sell += 10
    if not trend_wyzszy_ok: p_sell += 25
    else: p_sell -= 20

    # Ustalenie dominującego sygnału
    if p_buy >= 65:
        final_sig = "KUP"
        final_chance = p_buy
    elif p_sell >= 65:
        final_sig = "SPRZEDAJ"
        final_chance = p_sell
    else:
        final_sig = "CZEKAJ"
        final_chance = max(p_buy, p_sell)

    return {
        "Instrument": symbol.replace("-USD", ""),
        "Sygnał": final_sig,
        "Szansa %": int(min(max(final_chance, 0), 100)),
        "Trend Wyższy": "WZROST" if trend_wyzszy_ok else "SPADEK",
        "Cena": round(cena, 4),
        "RSI": round(rsi, 1),
        "Szansa KUP": int(p_buy),
        "Szansa SELL": int(p_sell),
        "ATR (Zmienność)": round(atr, 4)
    }

# --- UI ---
st.title("⚖️ Logiczny Skaner Kierunkowy")

wybrany_interwal = st.select_slider("Interwał:", options=list(interval_map.keys()), value="1 godz")

if st.button("🚀 ANALIZUJ", use_container_width=True):
    wyniki = []
    with st.spinner('Synchronizacja danych...'):
        for s in KRYPTO_LISTA:
            res = wykonaj_analize(s, wybrany_interwal)
            if res: wyniki.append(res)
    
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        
        def color_logic(row):
            if row['Sygnał'] == 'KUP': return ['background-color: #004d00'] * len(row)
            if row['Sygnał'] == 'SPRZEDAJ': return ['background-color: #4d0000'] * len(row)
            return [''] * len(row)

        st.dataframe(df_final.style.apply(color_logic, axis=1), use_container_width=True)
        
        st.divider()
        st.subheader("📋 Kalkulator Zleceń (Wybierz kierunek)")
        sel = st.selectbox("Wybierz krypto:", df_final['Instrument'])
        kierunek = st.radio("Wybierz kierunek zlecenia:", ["KUPNO (Long)", "SPRZEDAŻ (Short)"])
        
        d = df_final[df_final['Instrument'] == sel].iloc[0]
        cena, atr = d['Cena'], d['ATR (Zmienność)']
        
        c1, c2, c3 = st.columns(3)
        if kierunek == "KUPNO (Long)":
            c1.metric("Wejście", cena)
            c2.metric("Take Profit", round(cena + (atr * 3), 4))
            c3.metric("Stop Loss", round(cena - (atr * 1.5), 4))
        else:
            c1.metric("Wejście", cena)
            c2.metric("Take Profit", round(cena - (atr * 3), 4))
            c3.metric("Stop Loss", round(cena + (atr * 1.5), 4))
