import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# ... (poprzednie ustawienia interwałów i listy bez zmian) ...
interval_map = {"1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"}
KRYPTO_LISTA = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD"]

def wykonaj_analize(symbol, interwal_label):
    interwal = interval_map[interwal_label]
    try:
        df = yf.download(symbol, period="100d", interval=interwal, progress=False)
        if df.empty or len(df) < 50: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        # Wskaźniki
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.ema(length=50, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.macd(append=True)
        
        last = df.iloc[-1]
        cena_akt = float(last['Close'])
        ema20 = float(last['EMA_20'])
        atr = float(last['ATRr_14'])
        rsi = float(last['RSI_14'])
        
        # Obliczanie punktacji (uproszczone dla czytelności)
        score = 0
        if cena_akt > ema20: score += 20
        if rsi < 40: score += 20
        
        # --- NOWA LOGIKA: SUGEROWANE WEJŚCIE ---
        # Strategia: Wejście blisko EMA20 (tzw. mean reversion)
        if cena_akt > ema20: # W trendzie wzrostowym czekamy na korektę do średniej
            wejscie = max(ema20, cena_akt * 0.995) 
            sig = "KUP"
        else:
            wejscie = min(ema20, cena_akt * 1.005)
            sig = "SPRZEDAJ"

        return {
            "Instrument": symbol.replace("-USD", ""),
            "Sygnał": sig,
            "Cena rynkowa": round(cena_akt, 4),
            "Sugerowane Wejście": round(wejscie, 4), # To jest cena zlecenia LIMIT
            "TP (Cel)": round(wejscie + (atr * 2.5) if sig == "KUP" else wejscie - (atr * 2.5), 4),
            "SL (Stop)": round(wejscie - (atr * 1.5) if sig == "KUP" else wejscie + (atr * 1.5), 4),
            "RSI": round(rsi, 1)
        }
    except: return None

# --- UI (Tabela) ---
st.title("⚖️ Skaner PRO - Zoptymalizowane Wejścia")
interwal_sel = st.select_slider("Interwał:", options=list(interval_map.keys()), value="4 godz")

if st.button("🚀 ANALIZUJ"):
    wyniki = [res for s in KRYPTO_LISTA if (res := wykonaj_analize(s, interwal_sel))]
    if wyniki:
        df_final = pd.DataFrame(wyniki)
        st.dataframe(df_final.style.highlight_max(axis=0, subset=['Sugerowane Wejście']), use_container_width=True)
        st.caption("Sugerowane Wejście to cena Limit (oczekująca). Cena rynkowa to kurs 'na teraz'.")
