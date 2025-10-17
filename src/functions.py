import plotly.graph_objects as go

def format_timedelta(td_series):
    """Convert timedelta to readable format '00 hours and 00 minutes' """
    total_seconds = td_series.dt.total_seconds()
    hours = (total_seconds // 3600).astype(int)
    minutes = ((total_seconds % 3600) // 60).astype(int)
    return hours.astype(str) + ' hours and ' + minutes.astype(str).str.zfill(2) + ' minutes'

def index_recommendation(value):
    if value == 'Fear':
        return 'to buy.'
    elif value == 'Extreme Fear':
        return 'to buy.'
    elif value == 'Greed':
        return 'to sell.'
    elif value == 'Extreme Greed':
        return 'to sell.'
    
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def create_gauge(value):
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
        number = {'font': {'size': 40}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "black", 'thickness': 0.15},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': steps,
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor='white'
    ) 
    return fig
