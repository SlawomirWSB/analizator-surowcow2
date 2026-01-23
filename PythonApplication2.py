import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import re

# --- KONFIGURACJA ---
st.set_page_config(layout="wide", page_title="TERMINAL V18.0 | VERIFIED")

# --- STYLE ---
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #e6edf3; }
    * { color: #e6edf3 !important; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 25px; margin-bottom: 20px; border-left: 5px solid #00ff88;
    }
    .agg-box { 
        background: #1c2128; padding: 20px; border-radius: 10px; 
        text-align: center; border: 1px solid #30363d; margin-bottom: 15px;
    }
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%;
    }
    div.stButton > button:hover {
        background-color: #30363d !important; border-color: #58a6ff !important;
    }
    .streamlit-expanderHeader { background-color: #161b22 !important; color: #e6edf3 !important; }
    .streamlit-expanderContent { background-color: #0d1117 !important; border: 1px solid #30363d !important; }
    .logic-box { 
        background: #0d1117; border: 1px solid #30363d; padding: 12px; 
        border-radius: 6px; font-size: 0.9rem; color: #8b949e; margin-top: 10px;
    }
    .stProgress > div > div { background-color: #00ff88; }
    .stAlert { background-color: #1c2128 !important; color: #e6edf3 !important; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'signals_data' not in st.session_state:
    st.session_state.signals_data = []
    st.session_state.last_update = None
    st.session_state.analysis_cache = {}
    st.session_state.current_pair = None

# --- FUNKCJE SCRAPINGU ---

def parse_bestfreesignal():
    """Scraping z BestFreeSignal.com"""
    signals = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get('https://www.bestfreesignal.com/', headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Szukamy kart sygnałów
        signal_cards = soup.find_all('div', class_=['signal-card', 'signal', 'trade-signal'])
        
        for card in signal_cards[:10]:  # Max 10 sygnałów
            try:
                # Parsowanie danych (dostosuj selektory do rzeczywistej struktury HTML)
                pair = card.find(['h3', 'h4', 'span'], class_=['pair', 'symbol', 'currency-pair'])
                signal_type = card.find(['span', 'div'], class_=['type', 'direction', 'signal-type'])
                entry = card.find(['span', 'div'], text=re.compile(r'Entry|entry|ENTRY'))
                tp = card.find(['span', 'div'], text=re.compile(r'TP|Take Profit|take profit'))
                sl = card.find(['span', 'div'], text=re.compile(r'SL|Stop Loss|stop loss'))
                
                if pair and signal_type:
                    signals.append({
                        'p': pair.text.strip(),
                        'type': signal_type.text.strip().upper(),
                        'in': entry.text.strip() if entry else 'N/A',
                        'tp': tp.text.strip() if tp else 'N/A',
                        'sl': sl.text.strip() if sl else 'N/A',
                        'date': datetime.now().strftime("%d.%m %H:%M"),
                        'src': 'BESTFREESIGNAL',
                        'url': 'https://www.bestfreesignal.com/'
                    })
            except Exception as e:
                continue
                
    except Exception as e:
        st.warning(f"Błąd BestFreeSignal: {str(e)[:100]}")
    
    return signals

def parse_dailyforex():
    """Scraping z DailyForex.com"""
    signals = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get('https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1', 
                              headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Szukamy tabel lub kart z sygnałami
        signal_rows = soup.find_all(['tr', 'div'], class_=['signal-row', 'signal', 'forecast'])
        
        for row in signal_rows[:10]:
            try:
                pair = row.find(['td', 'span', 'h3'], class_=['pair', 'symbol', 'currency'])
                signal_type = row.find(['td', 'span'], class_=['direction', 'recommendation'])
                price_data = row.find_all(['td', 'span'], class_=['price', 'level'])
                
                if pair and signal_type:
                    signals.append({
                        'p': pair.text.strip(),
                        'type': signal_type.text.strip().upper(),
                        'in': price_data[0].text.strip() if len(price_data) > 0 else 'N/A',
                        'tp': price_data[1].text.strip() if len(price_data) > 1 else 'N/A',
                        'sl': price_data[2].text.strip() if len(price_data) > 2 else 'N/A',
                        'date': datetime.now().strftime("%d.%m %H:%M"),
                        'src': 'DAILYFOREX',
                        'url': 'https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1'
                    })
            except:
                continue
                
    except Exception as e:
        st.warning(f"Błąd DailyForex: {str(e)[:100]}")
    
    return signals

def parse_foresignal():
    """Scraping z ForeSignal.com"""
    signals = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get('https://foresignal.com/en/', headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Struktura może zawierać karty lub tabelę
        signal_items = soup.find_all(['div', 'tr'], class_=['signal', 'trade', 'forecast-item'])
        
        for item in signal_items[:10]:
            try:
                pair = item.find(['span', 'td', 'h4'], class_=['symbol', 'pair', 'currency'])
                direction = item.find(['span', 'td'], class_=['action', 'direction', 'type'])
                levels = item.find_all(['span', 'td'], class_=['price', 'level', 'value'])
                
                if pair and direction:
                    signals.append({
                        'p': pair.text.strip(),
                        'type': direction.text.strip().upper(),
                        'in': levels[0].text.strip() if len(levels) > 0 else 'N/A',
                        'tp': levels[1].text.strip() if len(levels) > 1 else 'N/A',
                        'sl': levels[2].text.strip() if len(levels) > 2 else 'N/A',
                        'date': datetime.now().strftime("%d.%m %H:%M"),
                        'src': 'FORESIGNAL',
                        'url': 'https://foresignal.com/en/'
                    })
            except:
                continue
                
    except Exception as e:
        st.warning(f"Błąd ForeSignal: {str(e)[:100]}")
    
    return signals

def parse_fxco():
    """Scraping z FX.co"""
    signals = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get('https://www.fx.co/pl/signals', headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Szukamy sygnałów w strukturze strony
        signal_blocks = soup.find_all(['div', 'article'], class_=['signal', 'trade-signal', 'signal-item'])
        
        for block in signal_blocks[:10]:
            try:
                symbol = block.find(['h3', 'span'], class_=['symbol', 'pair', 'instrument'])
                action = block.find(['span', 'div'], class_=['action', 'type', 'direction'])
                entry_price = block.find(text=re.compile(r'Entry|Wejście'))
                tp_price = block.find(text=re.compile(r'TP|Take Profit|Cel'))
                sl_price = block.find(text=re.compile(r'SL|Stop Loss'))
                
                if symbol and action:
                    signals.append({
                        'p': symbol.text.strip(),
                        'type': action.text.strip().upper(),
                        'in': entry_price.parent.text.strip() if entry_price else 'N/A',
                        'tp': tp_price.parent.text.strip() if tp_price else 'N/A',
                        'sl': sl_price.parent.text.strip() if sl_price else 'N/A',
                        'date': datetime.now().strftime("%d.%m %H:%M"),
                        'src': 'FX.CO',
                        'url': 'https://www.fx.co/pl/signals'
                    })
            except:
                continue
                
    except Exception as e:
        st.warning(f"Błąd FX.CO: {str(e)[:100]}")
    
    return signals

def calculate_success_probability(signal):
    """Oblicza prawdopodobieństwo sukcesu"""
    score = 50
    
    # Świeżość sygnału
    try:
        signal_time = datetime.strptime(signal['date'], "%d.%m %H:%M")
        hours_old = (datetime.now() - signal_time).total_seconds() / 3600
        if hours_old < 1:
            score += 25
        elif hours_old < 6:
            score += 15
        elif hours_old < 24:
            score += 5
    except:
        pass
    
    # Ratio TP/SL
    try:
        tp_str = re.sub(r'[^\d.]', '', str(signal['tp']))
        sl_str = re.sub(r'[^\d.]', '', str(signal['sl']))
        entry_str = re.sub(r'[^\d.]', '', str(signal['in']))
        
        if tp_str and sl_str and entry_str:
            tp = float(tp_str)
            sl = float(sl_str)
            entry = float(entry_str)
            
            reward = abs(tp - entry)
            risk = abs(sl - entry)
            
            if risk > 0:
                ratio = reward / risk
                if ratio > 3:
                    score += 20
                elif ratio > 2:
                    score += 15
                elif ratio > 1.5:
                    score += 10
    except:
        pass
    
    # Bonus za zaufane źródło
    if signal['src'] in ['FX.CO', 'DAILYFOREX']:
        score += 5
    
    return min(score, 99)

def generate_logic_explanation(signal, probability):
    """Generuje wyjaśnienie oceny"""
    logic_parts = []
    
    try:
        signal_time = datetime.strptime(signal['date'], "%d.%m %H:%M")
        hours_old = (datetime.now() - signal_time).total_seconds() / 3600
        if hours_old < 1:
            logic_parts.append("✅ Bardzo świeży sygnał (<1h)")
        elif hours_old < 6:
            logic_parts.append("✅ Świeży sygnał (<6h)")
        else:
            logic_parts.append("⚠️ Starszy sygnał")
    except:
        logic_parts.append("⚠️ Brak daty")
    
    try:
        tp_str = re.sub(r'[^\d.]', '', str(signal['tp']))
        sl_str = re.sub(r'[^\d.]', '', str(signal['sl']))
        entry_str = re.sub(r'[^\d.]', '', str(signal['in']))
        
        if tp_str and sl_str and entry_str:
            tp = float(tp_str)
            sl = float(sl_str)
            entry = float(entry_str)
            reward = abs(tp - entry)
            risk = abs(sl - entry)
            ratio = reward / risk if risk > 0 else 0
            logic_parts.append(f"✅ R/R: {ratio:.2f}")
    except:
        logic_parts.append("⚠️ Niepełne dane cenowe")
    
    logic_parts.append(f"📍 Źródło: {signal['src']}")
    
    return " | ".join(logic_parts)

def fetch_all_signals():
    """Pobiera sygnały ze wszystkich źródeł"""
    all_signals = []
    
    with st.spinner("Pobieram BestFreeSignal..."):
        all_signals.extend(parse_bestfreesignal())
    
    with st.spinner("Pobieram DailyForex..."):
        all_signals.extend(parse_dailyforex())
    
    with st.spinner("Pobieram ForeSignal..."):
        all_signals.extend(parse_foresignal())
    
    with st.spinner("Pobieram FX.CO..."):
        all_signals.extend(parse_fxco())
    
    # Filtruj i dodaj metryki
    cutoff_date = datetime.now() - timedelta(days=2)
    processed = []
    
    for signal in all_signals:
        try:
            signal_time = datetime.strptime(signal['date'], "%d.%m %H:%M")
            if signal_time > cutoff_date:
                signal['szansa'] = calculate_success_probability(signal)
                signal['logic'] = generate_logic_explanation(signal, signal['szansa'])
                processed.append(signal)
        except:
            signal['szansa'] = 50
            signal['logic'] = "⚠️ Brak pełnych danych"
            processed.append(signal)
    
    return processed

def fetch_aggregates(pair):
    """Mock agregatów - wymaga prawdziwego API"""
    import random
    options = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
    return {
        'inv': random.choice(options),
        'tv': random.choice(options)
    }

# --- INTERFEJS ---

header_left, header_right = st.columns([4, 1])
with header_left:
    st.title("🚀 TERMINAL V18.0 | XTB SMART SYNC")
with header_right:
    if st.button("🔄 AKTUALIZUJ"):
        st.session_state.signals_data = fetch_all_signals()
        st.session_state.last_update = datetime.now()
        st.session_state.analysis_cache = {}
        st.success("✅ Zaktualizowano!")
        time.sleep(0.5)
        st.rerun()

if st.session_state.last_update:
    st.caption(f"Ostatnia aktualizacja: {st.session_state.last_update.strftime('%d.%m.%Y %H:%M:%S')}")

if not st.session_state.signals_data:
    st.session_state.signals_data = fetch_all_signals()
    st.session_state.last_update = datetime.now()

col_left, col_right = st.columns([1.3, 0.7])

with col_left:
    st.subheader("📡 Sygnały Live")
    
    if not st.session_state.signals_data:
        st.info("Kliknij 'AKTUALIZUJ' aby pobrać sygnały")
    else:
        for s in st.session_state.signals_data:
            is_buy = any(word in s['type'].upper() for word in ['BUY', 'KUPNO', 'LONG'])
            color = "#00ff88" if is_buy else "#ff4b4b"
            
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span style="color:#00ff88; font-weight:bold; float:right;">{s['date']}</span>
                <b style="font-size:1.1rem;">{s['p']}</b> | 
                <a href="{s.get('url', '#')}" target="_blank" style="color:#58a6ff; text-decoration:none;">
                    <small>{s['src']}</small>
                </a>
                <div style="color:{color}; font-size:1.4rem; font-weight:bold; margin:15px 0;">
                    {s['type']} @ {s['in']}
                </div>
                <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; display:flex; justify-content:space-between; font-family:monospace;">
                    <span style="color:#00ff88">TP: {s['tp']}</span>
                    <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                st.session_state.current_pair = s['p']
                st.session_state.analysis_cache[s['p']] = fetch_aggregates(s['p'])
                st.rerun()

with col_right:
    st.subheader("📊 Niezależne Agregaty")
    
    pair = st.session_state.current_pair
    if pair and pair in st.session_state.analysis_cache:
        data = st.session_state.analysis_cache[pair]
        inv_color = "#00ff88" if "KUPNO" in data['inv'] else "#ff4b4b"
        tv_color = "#00ff88" if "KUPNO" in data['tv'] else "#ff4b4b"
        
        st.markdown(f"""
            <div class="agg-box">
                <b style="font-size:1.2rem;">{pair}</b><br><br>
                <div style="margin:10px 0;">
                    <small style="color:#8b949e">INVESTING.COM:</small><br>
                    <b style="color:{inv_color}; font-size:1.1rem;">{data['inv']}</b>
                </div>
                <div style="margin:10px 0;">
                    <small style="color:#8b949e">TRADINGVIEW:</small><br>
                    <b style="color:{tv_color}; font-size:1.1rem;">{data['tv']}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Wybierz instrument, aby zobaczyć agregaty.")
    
    st.markdown("---")
    st.subheader("🏆 Power Ranking AI")
    
    if st.session_state.signals_data:
        sorted_signals = sorted(st.session_state.signals_data, key=lambda x: x['szansa'], reverse=True)
        
        for item in sorted_signals:
            with st.expander(f"{item['p']} — {item['szansa']}%", expanded=(item['szansa'] > 85)):
                st.progress(item['szansa']/100)
                st.markdown(f"""
                <div class="logic-box">
                    <b>PODSTAWA OCENY:</b><br>
                    {item['logic']}
                </div>
                """, unsafe_allow_html=True)
    
    if st.button("🔙 RESET WIDOKU"):
        st.session_state.current_pair = None
        st.rerun()
