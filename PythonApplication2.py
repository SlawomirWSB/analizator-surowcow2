import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO - Ultra Stabilny", layout="wide")

KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", 
    "UNI-USD", "ATOM-USD", "ETC-USD", "XMR-USD", "ALGO-USD", "AAVE-USD", "VET-USD", "DOGE-USD"
]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

@st.cache_data(ttl=300) # Cache na 5 minut, aby oszczędzać limity Yahoo
def pobierz_dane_bezpiecznie(interwal_label):
    interwal = interval_map[interwal_label]
    # Kluczowe: Dobór okresu tak, by zawsze starczyło na EMA/BB
    if interwal in ["5m", "15m", "30m"]: okres = "7d"
    elif interwal in ["1h", "4h"]: okres = "60d"
    elif interwal == "1d": okres = "1y"
    else: okres = "max"

    try:
        data = yf.download(KRYPTO_XTB, period=okres, interval=interwal, group_by='ticker', progress=False, timeout=30)
        return data
    except:
        return None

def analizuj(data, tryb):
    if data is None: return []
    wyniki = []
    
    for symbol in KRYPTO_XTB:
        try:
            df = data[symbol].dropna()
            if len(df) < 35: continue

            # Technika
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.bbands(length=20, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.atr(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            l = df.iloc[-1]
            prev = df.iloc[-2]
            cena = float(l['Close'])
            rsi = float(l['RSI_14'])
            ema20 = float(l['EMA_20'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1

            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            
            # Punktacja Siły
            score = 45
            if (sig == "KUP" and rsi < 50) or (sig == "SPRZEDAJ" and rsi > 50): score += 20
            if vol_ratio > 1.1: score += 15
            if l['ADX_14'] > 25: score += 15

            # Wstęgi & Dywergencja
            bb_s = "Wewnątrz"
            if cena > l['BBU_20_2.0']: bb_s = "Wybicie Górą"
            elif cena < l['BBL_20_2.0']: bb_s = "Wybicie Dołem"

            dyw = "BRAK"
            if sig == "KUP" and cena > prev['Close'] and rsi < prev['RSI_14']: dyw = "NIEDŹW."
            elif sig == "SPRZEDAJ" and cena < prev['Close'] and rsi > prev['RSI_14']: dyw = "BYCZA"

            wej = cena if tryb == "rynkowy" else ema20
            atr = l['ATRr_14']

            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(score, 98),
                "Cena Wejścia": round(wej, 4),
                "Wolumen %": round(vol_ratio * 100),
                "RSI": round(rsi, 1),
                "ADX": round(l['ADX_14'], 1),
                "BB Status": bb_s,
                "Dyw.": dyw,
                "TP": round(wej + (atr*2.5) if sig=="KUP" else wej - (atr*2.5), 4),
                "SL": round(wej - (atr*1.5) if sig=="KUP" else wej + (atr*1.5), 4)
            })
        except: continue
    return wyniki

def stylizuj(df):
    def apply_row(row):
        s = [''] * len(row)
        sig = row['Sygnał']
        # Kolorowanie Sygnału (Tło)
        s[1] = 'background-color: #1e4620; color: white' if sig == 'KUP' else 'background-color: #5f1a1d; color: white'
        # Kolorowanie Siły (Tekst)
        s[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else 'color: #ff4b4b'
        # Wolumen & RSI (Warunkowe kolory tekstów)
        s[4] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        if sig == "KUP":
            s[5] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            s[5] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
        return s
    return df.style.apply(apply_row, axis=1)

# --- UI ---
st.title("⚖️ Skaner PRO - Wersja Precyzyjna")

int_sel = st.select_slider("Interwał:", options=list(interval_map.keys()), value="4 godz")

col1, col2 = st.columns(2)
with col1: btn_m = st.button("🚀 ANALIZA RYNKOWA", use_container_width=True)
with col2: btn_s = st.button("💎 ANALIZA LIMIT (EMA20)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    raw = pobierz_dane_bezpiecznie(int_sel)
    if raw is not None:
        final = analizuj(raw, mode)
        if final:
            df_res = pd.DataFrame(final).sort_values(by="Siła %", ascending=False)
            st.dataframe(stylizuj(df_res), use_container_width=True)
            st.info("Dane zbuforowane na 5 min. Zmiana trybu przyciskiem nie obciąża serwera.")
        else:
            st.warning("Pobrano dane, ale brak historii do obliczenia wskaźników. Wybierz mniejszy interwał.")
    else:
        st.error("Yahoo blokuje zapytania. Odczekaj 2 minuty przed kolejnym skanem.")
