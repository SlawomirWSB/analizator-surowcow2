with tab1:
        # Panel Wyboru
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        symbol = DB[rynek][inst]

        # --- DWA RÓŻNE WIDGETY ANALIZY ---
        st.subheader("🤖 Kompleksowa Analiza Techniczna")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:#83888D;'>Sygnał Główny (Zegar)</p>", unsafe_allow_html=True)
            tech_code = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{itv}m" if "{itv}".isdigit() else "1D",
              "width": "100%", "height": 450,
              "isTransparent": true, "symbol": "{symbol}",
              "showIntervalTabs": false, "displayMode": "single",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_code, height=470)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:#83888D;'>Wskaźniki Techniczne (Lista)</p>", unsafe_allow_html=True)
            # Zmieniony tryb wyświetlania na 'multiple' z włączonymi zakładkami interwałów
            detailed_code = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{itv}m" if "{itv}".isdigit() else "1D",
              "width": "100%", "height": 450,
              "isTransparent": true, "symbol": "{symbol}",
              "showIntervalTabs": true,
              "displayMode": "multiple",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(detailed_code, height=470)

        # Wykres Główny
        st.markdown("---")
        # ... reszta kodu (wykres) bez zmian ...
