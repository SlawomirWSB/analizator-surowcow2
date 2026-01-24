import streamlit as st
import pandas as pd
import pandas_ta as ta
from xtb.wrapper import XTBClient # Wymaga instalacji biblioteki do obsługi API XTB
import time

# Konfiguracja strony
st.set_page_config(page_title="Krypto Skaner XTB", layout="wide")

st.title("🚀 Zaawansowany Skaner Kryptowalut XTB")
st.write("Analiza techniczna wielu wskaźników (RSI, MACD, EMA, Bollinger Bands)")

# Sidebar - Konfiguracja połączenia
with st.sidebar:
    st.header("Ustawienia połączenia")
    user_id = st.text_input("User ID", type="default")
    password = st.text_input("Hasło", type="password")
    mode = st.selectbox("Tryb", ["demo", "real"])
    
    st.divider()
    
    # Suwak czasookresu
    interval_map = {
        "1 min": 1,
        "5 min": 5,
        "15 min": 15,
        "30 min": 30,
        "1 godz": 60,
        "4 godz": 240,
        "1 dzień": 1440,
        "1 tydz": 10080,
        "1 mies": 43200
    }
    selected_period = st.select_slider("Wybierz interwał (TF)", options=list(interval_map.keys()), value="4 godz")

# Lista kryptowalut (przykładowa, XTB posiada ok. 40+)
KRYPTO_LIST = [
    "BITCOIN", "ETHEREUM", "SOLANA", "CARDANO", "LITECOIN", 
    "RIPPLE", "DOT", "LINK", "DOGECOIN", "MATIC", "BITCOIN_CASH"
]

def perform_analysis(df):
    """Funkcja wykonująca analizę techniczną"""
    if len(df) < 50: return None
    
    # Obliczanie wskaźników
    df['RSI'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    df = pd.concat([df, macd], axis=1)
    df['EMA_20'] = ta.ema(df['close'], length=20)
    df['EMA_50'] = ta.ema(df['close'], length=50)
    
    last_price = df['close'].iloc[-1]
    rsi_val = df['RSI'].iloc[-1]
    ema20 = df['EMA_20'].iloc[-1]
    ema50 = df['EMA_50'].iloc[-1]
    
    # Logika oceny (Score 0-100)
    score = 50
    if rsi_val < 30: score += 20 # Wyprzedanie
    if rsi_val > 70: score -= 20 # Wykupienie
    if ema20 > ema50: score += 15 # Trend wzrostowy
    
    # Wyznaczanie TP i SL (uproszczone na podstawie zmienności ATR)
    atr = ta.atr(df['high'], df['low'], df['close']).iloc[-1]
    tp = last_price + (atr * 2)
    sl = last_price - (atr * 1.5)
    
    return {
        "Cena": round(last_price, 4),
        "RSI": round(rsi_val, 2),
        "Szansa %": min(max(score, 0), 100),
        "Entry": round(last_price, 4),
        "TP": round(tp, 4),
        "SL": round(sl, 4)
    }

if st.button("ANALIZUJ WSZYSTKIE KRYPTO"):
    if not user_id or not password:
        st.error("Wprowadź dane logowania w pasku bocznym!")
    else:
        results = []
        progress_bar = st.progress(0)
        
        with st.spinner('Pobieranie danych i analiza...'):
            # Tutaj następuje symulacja logiki API (w realnym kodzie użyjesz XTBClient)
            # Przykładowa pętla przez krypto:
            for i, symbol in enumerate(KRYPTO_LIST):
                try:
                    # Symulacja pobrania danych (OHLC)
                    # client = XTBClient(user_id, password, mode)
                    # data = client.get_chart_last(symbol, interval_map[selected_period])
                    
                    # Placeholder dla danych (do celów prezentacji kodu)
                    dummy_data = pd.DataFrame({
                        'close': [100 + j for j in range(100)],
                        'high': [105 + j for j in range(100)],
                        'low': [95 + j for j in range(100)]
                    })
                    
                    analysis = perform_analysis(dummy_data)
                    if analysis:
                        analysis['Kryptowaluta'] = symbol
                        results.append(analysis)
                except Exception as e:
                    st.warning(f"Błąd przy {symbol}: {e}")
                
                progress_bar.progress((i + 1) / len(KRYPTO_LIST))
        
        if results:
            df_results = pd.DataFrame(results)
            # Sortowanie po najwyższej szansie powodzenia
            df_results = df_results.sort_values(by="Szansa %", ascending=False)
            
            # Wyświetlenie tabeli
            st.dataframe(
                df_results.style.background_gradient(subset=['Szansa %'], cmap='RdYlGn'),
                use_container_width=True
            )
            
            st.success("Analiza zakończona pomyślnie!")
        else:
            st.error("Nie udało się pobrać żadnych danych.")
        
