import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

#configure the page
st.set_page_config(
    page_title='Check Fear & Greed Index',
    layout='wide',
    page_icon=':memo:'
)

#connect to the database
@st.cache_resource
def get_database_connection():
    database_url = 'postgresql+psycopg2://admin:admin@localhost:5432/Dashboard'
    return create_engine(database_url)

#load the data from the database
def load_data():
    engine = get_database_connection()
    query = 'SELECT * FROM fear_greed_index ORDER BY date_index ASC'
    df = pd.read_sql(query, engine)
    return df

#create gauge
def create_gauge(value, title):
    if value <= 25:
        color = 'red'
    elif value <= 50:
        color = 'orange'
    elif value <= 75:
        color = 'yellow'
    elif value <= 100:
        color = 'lightgreen'
    
    fig = go.Figure(go.Indicator(
        mode = 'gauge+number',
        value = value,
        title = {'text': title},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': 'rgba(0,0,0,0)'},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': "#9CA0A0",
            'steps': [
                {'range': [0, 24], 'color': 'red'},
                {'range': [25, 49], 'color': 'orange'},
                {'range': [50, 74], 'color': 'yellow'},
                {'range': [75, 100], 'color': 'lightgreen'}],
            'threshold': {'line': {'color': "#090213", 'width': 4}, 'thickness': 0.75, 'value': value}, 'shape': 'angular'},
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig

def make_call(value):
    if value <= 50:
        return 'buy.'
    else:
        return 'sell.'

def make_index(value):
    if value <= 24:
        return 'Extreme Fear'
    elif value <= 49:
        return 'Fear'
    elif value == 50:
        return 'Neutral'
    elif value <= 74:
        return 'Greed'
    elif value <= 100:
        return 'Extreme Greed'

def main():
    st.title('Check Fear & Greed Index')
    call = make_call(42)
    fgindex = make_index(42)
    st.sidebar.write(f'Crypto Fear & Greed Index is {fgindex}, and it tells you to {call}\n Should you?')

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig = create_gauge(42, 'Fear & Greed Index')
        st.plotly_chart(fig, use_container_width=True)

if __name__=='__main__':
    main()