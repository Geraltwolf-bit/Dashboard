import streamlit as st
import pandas as pd
import altair as alt

from stockmarket import get_raw_stockmarket_data, get_yearly_stockmarket_trend, get_montly_stockmarket_trend, get_yearly_stockmarket_data_for_dashboard

st.set_page_config(page_title='Stock Market Breakdown',
                   page_icon=':roller_coaster:',
                   layout='wide',
                   initial_sidebar_state='auto')

raw_sm = get_raw_stockmarket_data()

with st.sidebar:
    st.header('Stock Market Health')

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.header('Monthly trend')
    sm_month = get_montly_stockmarket_trend(raw_sm)
    month_chart = alt.Chart(sm_month).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta = 'stockmarket_value:Q',
        color = alt.value('#29b5e8')
    )
    st.altair_chart(month_chart)
      
with col2:
    sm = get_yearly_stockmarket_data_for_dashboard(raw_sm)
    st.area_chart(sm, x = 'date', y = 'stockmarket_value')

with col3:
    st.header('Yearly trend')
    sm_year = get_montly_stockmarket_trend(raw_sm)
    year_chart = alt.Chart(sm_year).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta = 'stockmarket_value:Q',
        color = alt.value("#3fe829"))
    st.altair_chart(year_chart)