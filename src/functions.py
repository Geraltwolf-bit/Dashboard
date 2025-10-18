import plotly.graph_objects as go
import streamlit as st
import altair as alt
from fg_index_year import get_fg_index_year
from constants import fg_year_url

def format_timedelta(td_series):
    """Convert timedelta to readable format '00 hours and 00 minutes' """
    total_seconds = td_series.dt.total_seconds()
    hours = (total_seconds // 3600).astype(int)
    minutes = ((total_seconds % 3600) // 60).astype(int)
    return hours.astype(str) + ' hours and ' + minutes.astype(str).str.zfill(2) + ' minutes'

def index_recommendation(value):
    if value == 'Fear':
        return 'to buy'
    elif value == 'Extreme Fear':
        return 'to buy'
    elif value == 'Greed':
        return 'to sell'
    elif value == 'Extreme Greed':
        return 'to sell'
    
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def create_gauge(value, title_text="Fear & Greed Index"):
    """
    Create a gauge with smooth gradient
    """
    # Create smooth gradient by adding many small steps
    steps = []
    for i in range(100):
        # Calculate color based on position (red -> yellow -> green)
        if i <= 50:
            # Red to Yellow
            r = 255
            g = int(255 * (i / 50))
            b = 0
        else:
            # Yellow to Green
            r = int(255 * (1 - (i - 50) / 50))
            g = 255
            b = 0
        color = f'rgb({r}, {g}, {b})'
        steps.append({'range': [i, i+1], 'color': color})
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title={'text': title_text, 'font': {'size': 15}},
        number = {'font': {'size': 18, 'color':  'black'},
                  'suffix': '',
                  'valueformat': 'd'},
        gauge = {
            'axis': {'range': [0, 100],
                     'showticklabels': False,
                     'ticks': '',
                     'tickwidth': 0},
            'bar': {'color': "rgba(0,0,0,0)"},
            'bgcolor': "white",
            'borderwidth': 0,
            'bordercolor': "gray",
            'steps': steps,
            'threshold': {
                'line': {'color': "black", 'width': 3},
                'thickness': 0.4,
                'value': value
            }
        }
    ))
    fig.update_layout(
        title={
            'text': title_text,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 15}
        },
        height=150,
        margin=dict(l=20, r=20, t=55, b=20),
        paper_bgcolor='white',
        font={'family': 'Arial'}
    ) 
    return fig

def create_chart(df):
    chart = alt.Chart(df).mark_line(
        color='orange',
        strokeWidth=3
    ).encode(
        x=alt.X('index_date:T', title='Date'),
        y=alt.Y('fg_index_num:Q', title='Fear&Greed Index', scale=alt.Scale(domain=[0,100])),
        tooltip=['index_date', 'fg_index_num', 'fg_index_str']
    ).properties(
        height=300
    ).interactive()
    return chart