import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
from fear_greed_index import get_df_fg_index_today
from functions import index_recommendation, create_gauge
from constants import fg_today_url

with st.sidebar:
    fg_index = get_df_fg_index_today(fg_today_url)
    rec = fg_index['fg_index_str'].iloc[0]
    today_date = datetime.now().strftime("%B, %d")
    st.title(f"{today_date}")
    st.title("Crypto Fear & Greed Index:")
    st.title(f'{rec}')
    recommendation = index_recommendation(rec)
    st.title(f"It tells you {recommendation}")
    st.title("But should you?")

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    index_num = int(fg_index['fg_index_num'].iloc[0])
    fig = create_gauge(index_num)
    st.plotly_chart(fig, use_container_width=True)