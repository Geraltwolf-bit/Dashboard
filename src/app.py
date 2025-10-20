import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime

from fear_greed_index import get_df_fg_index_today
from fg_index_year import get_fg_index_year
from functions import index_recommendation, create_gauge, create_chart
from constants import fg_today_url, fg_year_url
from stockmarket import get_raw_stockmarket_data, get_yearly_stockmarket_data_for_dashboard

with st.sidebar:
    fg_index = get_df_fg_index_today(fg_today_url)
    rec = fg_index['fg_index_str'].iloc[0]
    today_date = datetime.now().strftime("%B, %d")
    st.title(f"{today_date}")
    st.title("Crypto Fear & Greed Index:")
    st.title(f'{rec}')
    recommendation = index_recommendation(rec)
    st.title(f"It tells you... {recommendation}")
    st.title("But should you?")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("Current index:")
    index_text = str(fg_index['fg_index_str'].iloc[0])
    st.subheader(f"{index_text}")
    index_num = int(fg_index['fg_index_num'].iloc[0])
    fig = create_gauge(
        value=index_num,
        title_text=f"Fear & Greed Index: {index_text}")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.header("Historical trend")
    df = get_fg_index_year(fg_year_url)
    chart = create_chart(df)
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.header('Stockmarket trend')
    raw_sm = get_raw_stockmarket_data()
    sm = get_yearly_stockmarket_data_for_dashboard(raw_sm)
    st.line_chart(sm, x='date', y='stockmarket_value')