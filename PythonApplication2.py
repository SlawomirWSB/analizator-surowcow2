import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner Krypto LOGIC v3", layout="wide")

KRYPTO_LISTA = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "DOGE-USD", "AVAX-USD", "BCH-USD",
    "SHIB-USD", "ALGO-USD", "UNI-USD", "NEAR-USD", "ATOM-USD", "ICP-USD"
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
    # Optymalizacja okresu pobierania danych
    okres_map = {"1m": "1d", "5m": "1d", "15m": "1d", "30m": "1d", "1h": "1mo", "1d": "2y", "1wk": "max", "1mo": "max"}
    
    df = pobierz_dane(symbol, interwal, okres_map.get(interwal, "2y"))
    if df.empty or len(df) < 30: return None

    df.ta.rsi(length=14, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.atr(length=14, append=True)

    last = df.iloc[-1]
    prev = df.iloc[-2]
    cena = float(last['Close'])
    rsi = float(last['RSI_14'])
    atr = float(last['ATRr_14'])
    
    # TREND WYŻSZY (MTF)
    tf_wyzszy = "1d" if "m" in interwal or "h" in interwal else "1wk"
    df_big = pobierz_dane(symbol, tf_wyzszy, "2y")
    trend_wyzszy_ok = True
    if not df_big.empty and len(df_big) > 20:
        ema_big = ta.ema(df_big['Close'], length=20)
        trend_wyzszy_ok = float(df_big['Close'].iloc[-1]) > float(ema_big.iloc[-1])

    # --- ZBALANSOWANY SCORING ---
    # Punkty bazowe
    p_buy = 40
    p_sell = 40

    # Analiza RSI (Lokalna)
    if rsi < 30: p_buy += 25  # Wyprzedanie - silny sygnał kupna
    elif rsi < 45: p_buy += 10
    
    if rsi > 70: p_sell += 25 # Wykupienie - silny sygnał sprzedaży
    elif rsi > 55: p_sell += 10

    # Analiza Ceny względem EMA (Lokalna)
    if cena > last['EMA_20']: p_buy += 15
    else: p_sell += 15

    # Momentum (czy cena rośnie względem poprzedniej świecy)
    if cena > prev['Close']: p_buy += 10
    else: p_sell += 10

    # Wpływ Trendu Wyższego (Złagodzony)
    if trend_wyzszy_ok: p_buy += 10
    else: p_sell += 10

    # FINALIZACJA SYGNAŁU
    # Próg sygnału obniżony do 60% dla większej czułości
    if p_buy > p_sell and p_buy >= 60:
        final_sig, main_chance, oppo_chance = "KUP", p_buy, p_sell
    elif p_sell > p_buy and p_sell >= 60:
        final_sig, main_chance, oppo_chance = "SPRZEDAJ", p_sell, p_buy
    else:
        final_sig, main_chance, oppo_chance = "CZEKAJ", max(p_buy, p_sell), min(p_buy, p_sell)

    return {
        "Instrument": symbol.replace("-USD", ""),
        "Sygnał": final_sig,
        "Szansa %": int(min(max(main_chance, 0), 100)),
        "Opozycja %": int(min(max(oppo_chance, 0), 100)),
        "Trend Wyższy": "WZROST" if trend_wyzszy_ok else "SPADEK",
        "Cena": round(cena, 4),
        "RSI": round(rsi, 1),
        "ATR_VAL": atr
    }

# --- UI ---
st.title("⚖️ Zbalansowany Skaner Kierunkowy")

interwal_sel = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="1 godz")

if st.button("🚀 ANALIZUJ RYNEK", use_container_width=True):
    wyniki = []
    with st.spinner('Przeliczanie wskaźników...'):
        for s in KRYPTO_LISTA:
            res = wykonaj_analize(s, interwal_sel)
            if res: wyniki.append(res)
    
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        
        def style_logic(row):
            if row['Sygnał'] == 'KUP':
                return ['background-color: #28a745; color: white; font-weight: bold'] * len(row)
            if row['Sygnał'] == 'SPRZEDAJ':
                return ['background-color: #dc3545; color: white; font-weight: bold'] * len(row)
            return ['color: white'] * len(row)

        cols = ["Instrument", "Sygnał", "Szansa %", "Opozycja %", "Trend Wyższy", "Cena", "RSI"]
        st.dataframe(df_final[cols].style.apply(style_logic, axis=1), use_container_width=True, height=600)
        
        # KALKULATOR
        st.divider()
        st.subheader("📋 Kalkulator Zleceń")
        sel_inst = st.selectbox("Wybierz instrument:", df_final['Instrument'])
        kier = st.radio("Kierunek:", ["KUPNO", "SPRZEDAŻ"])
        
        d = df_final[df_final['Instrument'] == sel_inst].iloc[0]
        c, a = d['Cena'], d['ATR_VAL']
        
        r1, r2, r3 = st.columns(3)
        if kier == "KUPNO":
            r1.metric("Wejście", c)
            r2.metric("TP (Profit)", round(c + (a * 2.5), 4))
            r3.metric("SL (Stop)", round(c - (a * 1.2), 4))
        else:
            r1.metric("Wejście", c)
            r2.metric("TP (Profit)", round(c - (a * 2.5), 4))
            r3.metric("SL (Stop)", round(c + (a * 1.2), 4))
