import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="Skaner Krypto PRO + Opozycja", layout="wide")

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

    # OBLICZENIA TECHNICZNE
    df.ta.rsi(length=14, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=50, append=True)
    df.ta.atr(length=14, append=True)
    df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()

    last = df.iloc[-1]
    cena = float(last['Close'])
    rsi = float(last['RSI_14'])
    atr = float(last['ATRr_14'])
    
    # FILTR TRENDU WYŻSZEGO (MTF)
    tf_wyzszy = "1d" if "m" in interwal or "h" in interwal else "1wk"
    df_big = pobierz_dane(symbol, tf_wyzszy, "2y")
    trend_wyzszy_ok = True
    if not df_big.empty and len(df_big) > 20:
        ema_big = ta.ema(df_big['Close'], length=20)
        trend_wyzszy_ok = float(df_big['Close'].iloc[-1]) > float(ema_big.iloc[-1])

    # SCORING KUP (Twoje obecne zasady)
    score_buy = 50
    if rsi < 30: score_buy += 15
    if rsi > 70: score_buy -= 20
    if cena > last['EMA_20'] > last['EMA_50']: score_buy += 15
    if last['Volume'] > last['Vol_Avg']: score_buy += 5
    if not trend_wyzszy_ok: score_buy -= 30 
    score_buy = int(min(max(score_buy, 0), 100))

    # SCORING OPOZYCJA (SPRZEDAJ)
    score_sell = 50
    if rsi > 70: score_sell += 20
    if rsi < 30: score_sell -= 15
    if cena < last['EMA_20'] < last['EMA_50']: score_sell += 15
    if last['Volume'] > last['Vol_Avg']: score_sell += 5
    if trend_wyzszy_ok: score_sell -= 20 # Kara dla sprzedaży, gdy trend dzienny rośnie
    score_sell = int(min(max(score_sell, 0), 100))

    signal = "KUP" if score_buy >= 65 else "SPRZEDAJ" if score_buy <= 35 else "CZEKAJ"
    
    # Parametry dla KUP (wymuszone dla opozycji)
    tp_buy = cena + (atr * 3)
    sl_buy = cena - (atr * 1.5)
    zysk_buy = ((tp_buy - cena) / cena) * 100

    return {
        "Instrument": symbol.replace("-USD", ""),
        "Sygnał": signal,
        "Szansa %": score_buy,
        "Opozycja (Sprzedaż) %": score_sell,
        "Trend Wyższy": "WZROST" if trend_wyzszy_ok else "SPADEK",
        "Cena": round(cena, 4),
        "Zysk do TP (KUP)": f"{round(zysk_buy, 2)}%",
        "RSI": round(rsi, 1),
        "Wejście KUP": round(cena, 4),
        "TP KUP": round(tp_buy, 4),
        "SL KUP": round(sl_buy, 4)
    }

# --- UI ---
st.title("🛡️ Skaner Krypto PRO + Analiza Opozycji")

wybrany_interwal = st.select_slider("Zmień interwał analizy:", options=list(interval_map.keys()), value="1 godz")

if st.button("🚀 URUCHOM ANALIZĘ", use_container_width=True):
    wyniki = []
    with st.spinner('Przeliczanie szans i opozycji...'):
        for s in KRYPTO_LISTA:
            res = wykonaj_analize(s, wybrany_interwal)
            if res: wyniki.append(res)
    
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        
        # Stylizacja
        def style_rows(row):
            if row['Sygnał'] == 'KUP' and row['Trend Wyższy'] == 'WZROST':
                return ['background-color: #004d00; color: white'] * len(row)
            if row['Opozycja (Sprzedaż) %'] > 60:
                return ['color: #ffb3b3'] * len(row) # Jasny czerwony dla silnej opozycji
            return [''] * len(row)

        st.dataframe(df_final.style.apply(style_rows, axis=1), use_container_width=True, height=800)
        
        # Sekcja szczegółów (po kliknięciu/wyborze)
        st.divider()
        st.subheader("💡 Kalkulator Wejścia (Opozycja/Kupno)")
        wybrany_inst = st.selectbox("Wybierz instrument, aby zobaczyć parametry KUP (nawet jeśli teraz spada):", df_final['Instrument'])
        
        row_sel = df_final[df_final['Instrument'] == wybrany_inst].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Cena Wejścia", row_sel['Wejście KUP'])
        c2.metric("Take Profit", row_sel['TP KUP'], f"+{row_sel['Zysk do TP (KUP)']}")
        c3.metric("Stop Loss", row_sel['SL KUP'], delta_color="inverse")
        c4.write(f"**Aktualna Szansa KUP:** {row_sel['Szansa %']}%")
        
    else:
        st.error("Błąd danych.")
