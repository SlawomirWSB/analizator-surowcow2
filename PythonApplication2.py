import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide", page_title="TERMINAL V5.1", initial_sidebar_state="collapsed")

# NOWE ŹRÓDŁA BEZ FXLEADERS
class SignalManager:
    SOURCES = {
        "BESTFREESIGNAL": "https://www.bestfreesignal.com",
        "ECONOMIES": "https://www.economies.com/investing/signals",
        "HOWTOTRADE": "https://howtotrade.com/free-forex-signals/",
        "STPTRADING": "https://www.stptrading.io/analysis/",
        "INVESTING": "https://www.investing.com/currencies/forex-signals"
    }
    
    @staticmethod
    def generate_signals(count=12):
        pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "Gold", "Crude Oil", "EUR/GBP"]
        symbols = {"EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "USD/JPY": "FX:USDJPY", 
                  "AUD/USD": "FX:AUDUSD", "USD/CAD": "FX:USDCAD", "Gold": "OANDA:XAUUSD", 
                  "Crude Oil": "TVC:USOIL", "EUR/GBP": "FX:EURGBP"}
        sources = list(SignalManager.SOURCES.keys())
        
        signals = []
        for i in range(count):
            now = datetime.now() - timedelta(hours=i*3)
            signal_type = random.choice(["KUPNO", "SPRZEDAŻ"])
            base_price = 1.0900 + (i * 0.001) if "USD" in pairs[i%len(pairs)] else 2650 + (i*5)
            
            signal = {
                "pair": pairs[i % len(pairs)],
                "sym": symbols[pairs[i % len(pairs)]],
                "date": now.strftime("%d.%m"),
                "hour": now.strftime("%H:%M"),
                "type": signal_type,
                "in": f"{base_price:.4f}" if base_price < 10 else f"{int(base_price)}",
                "sl": f"{base_price - 0.02 if signal_type=='KUPNO' else base_price + 0.02:.4f}",
                "tp": f"{base_price + 0.06 if signal_type=='KUPNO' else base_price - 0.06:.4f}",
                "rsi_base": random.randint(35, 65),
                "src": sources[i % len(sources)],
                "url": SignalManager.SOURCES[sources[i % len(sourc
