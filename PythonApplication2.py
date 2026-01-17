Błąd wynika z tego, że w którymś z elementów `st.session_state.signals` nie ma klucza `"live"`, a tutaj:

```python
live_count = len([s for s in st.session_state.signals if s['live']])
```

odwołujesz się do niego „na sztywno”, więc dostajesz `KeyError`.

Najprostsza poprawka: użyj `dict.get()` z domyślną wartością (np. `False`) zamiast `s['live']`.  
Dodatkowo warto używać `get` też w innych miejscach, gdzie zakładasz istnienie klucza `"live"`.

Poniżej fragmenty wymagające zmiany (reszta kodu bez zmian):

```python
# --- GŁÓWNY FLOW, liczenie live_count ---
else:
    st.title("🚀 TERMINAL V6.0 | LIVE + AI SIGNALS")
    h1, h2, h3 = st.columns([2,1,1])
    with h1:
        # POPRAWKA – użyj get('live', False)
        live_count = len([s for s in st.session_state.signals if s.get('live', False)])
        st.markdown(
            f"**LIVE SIGNALS: {live_count} | AI: {len(st.session_state.signals)-live_count} | "
            f"NAJNOWSZE GÓRĄ**"
        )
```

oraz w dwóch miejscach, gdzie tworzysz opisy z ikonką:

```python
def render_signal_card(signal, idx):
    color = "#00ff88" if signal['type'] == "KUPNO" else "#ff4b4b"
    card_class = "live-signal" if signal.get('live', False) else "sim-signal"
    
    st.markdown(f"""
    <div class="signal-card {card_class}">
        ...
            <a href="{signal['url']}" target="_blank" 
               style="color: #00ff88; text-decoration: none; font-size: 0.75rem; 
                      padding: 4px 8px; border: 1px solid #00ff88; border-radius: 4px;">
               {signal['src']}{' 🔴' if signal.get('live', False) else ' 🟡'}
            </a>
        ...
    </div>
    """, unsafe_allow_html=True)
    ...
```

```python
def render_detail_view(signal):
    st.subheader(
        f"🔬 **{signal['pair']}** | {signal['type']} | Score: {signal['score']}% | "
        f"{signal['src']}{' 🔴 LIVE' if signal.get('live', False) else ' 🟡 AI'}"
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        ...
        if signal.get('live', False):
            st.markdown(
                f'<div class="agg-box"><div style="font-size: 0.75rem; color: #8b949e;">Data</div>'
                f'<div style="font-size: 1.1rem; font-weight: bold; color: #ffffff;">'
                f'{signal["full_date"]}</div></div>',
                unsafe_allow_html=True
            )
```

Po tych poprawkach brak klucza `"live"` w jakimkolwiek sygnale nie będzie już powodował błędu.
