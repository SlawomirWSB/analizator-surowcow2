# ... fragment kodu V69 ...
with col_r:
    item = DB[st.session_state.active]
    data_tf = item[global_tf]
    
    st.subheader(f"📊 Analiza ({global_tf}): {st.session_state.active}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="aggregator-card">
            <small>Investing.com (Trend)</small>
            <div style="color:{info['color']}; font-size:1.5rem; font-weight:900;">{data_tf['inv']}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="aggregator-card">
            <small>TradingView (Średnie)</small>
            <div style="color:{info['color']}; font-size:1.5rem; font-weight:900;">{data_tf['tv']}</div>
        </div>""", unsafe_allow_html=True)

    # NOWOŚĆ: Jasne rozbicie na Oscylatory (Twoje "12 sprzedaży")
    st.markdown(f"""
        <div class="aggregator-card">
            <p style="text-align:center; color:#b2b5be; margin-bottom:10px;">LICZNIK WSKAŹNIKÓW (OSCYLATORY)</p>
            <div style="display:flex; justify-content:space-around;">
                <div style="text-align:center;"><small>Sprzedaż</small><br><b style="color:#ff4b4b; font-size:1.4rem;">{data_tf['counts'].split('/')[0]}</b></div>
                <div style="text-align:center;"><small>Neutralnie</small><br><b style="color:#f39c12; font-size:1.4rem;">{data_tf['counts'].split('/')[1]}</b></div>
                <div style="text-align:center;"><small>Kupno</small><br><b style="color:#00ff88; font-size:1.4rem;">{data_tf['counts'].split('/')[2]}</b></div>
            </div>
            <p style="font-size:0.8rem; color:#8f94a1; margin-top:10px; text-align:center;">
                ⚠️ Rozbieżność: Średnie wskazują trend, ale oscylatory ({data_tf['counts'].split('/')[0]} sprz.) ostrzegają przed korektą.
            </p>
        </div>
    """, unsafe_allow_html=True)
# ... reszta kodu ...
