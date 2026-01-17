# Zmieniona metoda generująca sygnały
@staticmethod
def generate_signals(count=12):
    pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "Gold", "Crude Oil WTI", "EUR/GBP", "NZD/USD"]
    symbols = {
        "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "USD/JPY": "FX:USDJPY", 
        "AUD/USD": "FX:AUDUSD", "USD/CAD": "FX:USDCAD", "Gold": "OANDA:XAUUSD", 
        "Crude Oil WTI": "TVC:USOIL", "EUR/GBP": "FX:EURGBP", "NZD/USD": "FX:NZDUSD"
    }
    sources = list(SignalManager.SOURCES.keys())
    
    signals = []
    for i in range(count):
        now = datetime.now() - timedelta(minutes=i*45 + random.randint(0,30))
        signal_type = random.choice(["KUPNO", "SPRZEDAŻ"])
        
        # Ustalanie cen bazowych
        base_price = SignalManager.get_base_price(signal_type, pairs[i % len(pairs)], i)

        signal = {
            "pair": pairs[i % len(pairs)],
            "sym": symbols[pairs[i % len(pairs)]],
            "date": now.strftime("%Y-%m-%d %H:%M:%S"),  # Ustalona data aktualizacji
            "timestamp": now.timestamp(),
            "type": signal_type,
            "in": f"{base_price:.4f}" if base_price < 100 else f"{base_price:.2f}",
            # SL i TP
            "sl": SignalManager.calculate_sl_tp(base_price, sl_offset, signal_type, "sl"),
            "tp": SignalManager.calculate_sl_tp(base_price, tp_offset, signal_type, "tp"),
            "rsi_base": random.randint(28, 72),
            "src": sources[i % len(sources)],
            "url": SignalManager.SOURCES[sources[i % len(sources)]],
            "score": random.randint(82, 98),
            "inv": random.choice(["KUPNO", "SPRZEDAŻ", "NEUTRAL"]),
            "tv": random.choice(["SILNE KUPNO", "KUPNO", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]),
            "analysis": random.choice([
                "Wybicie z kanału H4", "RSI divergence", "Odbicie Fibonacci 61.8%", 
                "Breakout trendline", "Opór kluczowy 1D", "Wsparcie wielodniowe", "MACD crossover"
            ]),
            "ma20": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "ma50": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "macd": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "stoch": random.randint(20, 80)
        }
        signals.append(signal)

    # Dodajemy 5 pozycji z symulacji
    simulation_positions = SignalManager.get_simulation_positions()
    signals.extend(simulation_positions)

    return sorted(signals, key=lambda x: x['timestamp'], reverse=True)

@staticmethod
def get_base_price(signal_type, pair, index):
    if "Oil" in pair:
        return 72.50 + random.uniform(-1,1)
    elif "Gold" in pair:
        return 2650 + random.uniform(-10,10)
    else:
        return 1.0850 + (index * 0.0005) + random.uniform(-0.005,0.005)

@staticmethod
def calculate_sl_tp(base_price, offset, signal_type, tp_or_sl):
    if tp_or_sl == "sl":
        return f"{base_price - abs(offset):.4f}" if signal_type == "KUPNO" else f"{base_price + abs(offset):.4f}"
    else:  # tp
        return f"{base_price + offset:.4f}" if signal_type == "KUPNO" else f"{base_price - abs(offset):.4f}"

@staticmethod
def get_simulation_positions():
    # Przykładowe dane dla pozycji z symulacji
    simulation_positions = []
    for i in range(5):
        simulation_positions.append({
            "pair": f"SIMULATED_PAIR_{i+1}",
            "sym": f"SIM:PAIR_{i+1}",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": datetime.now().timestamp(),
            "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "in": f"{random.uniform(1.0, 2.0):.4f}",
            "sl": f"{random.uniform(0.5, 1.5):.4f}",
            "tp": f"{random.uniform(1.5, 2.5):.4f}",
            "rsi_base": random.randint(28, 72),
            "src": "Simulation",
            "url": "#",
            "score": random.randint(70, 90),
            "inv": random.choice(["KUPNO", "SPRZEDAŻ", "NEUTRAL"]),
            "tv": random.choice(["SILNE KUPNO", "KUPNO", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]),
            "analysis": "Symulacja pozycji",
            "ma20": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "ma50": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "macd": random.choice(["KUPNO", "SPRZEDAŻ"]),
            "stoch": random.randint(20, 80)
        })
    return simulation_positions
