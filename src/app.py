import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from database import get_db_engine
from fg_index_year import get_fg_index_year, scatter_index
from constants import fg_year_url
from database import get_db_engine
from sqlalchemy import create_engine

st.set_page_config(page_title='Fear & Greed Dashboard',
                   page_icon ='📊',
                   layout = 'wide',
                   initial_sidebar_state='expanded')
alt.themes.enable("dark")
# CSS styling
st.markdown("""
    <style>

    [data-testid="block-container"] {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-bottom: -7rem;
    }

    [data-testid="stVerticalBlock"] {
        padding-left: 0rem;
        padding-right: 0rem;
    }

    [data-testid="stMetric"] {
        background-color: #393939;
        text-align: center;
        padding: 15px 0;
    }

    [data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    [data-testid="stMetricDeltaIcon-Up"] {
        position: relative;
        left: 38%;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        transform: translateX(-50%);
    }

    [data-testid="stMetricDeltaIcon-Down"] {
        position: relative;
        left: 38%;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        transform: translateX(-50%);
    }

    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_data_connection():
    databese_url = 'postgresql://admin:admin@localhost:5432/Dashboard'
    return create_engine(databese_url)

def load_data():
    engine = get_db_engine()
    df_today = pd.read_sql("SELECT * FROM fear_greed_index", engine)
    return df_today


def create_gauge_chart(value, title):
    """Create a speedometer gauge chart for Fear & Greed Index"""
    #Determine bar color based on value
    if value <= 25:
        color = 'red'
    elif value <= 45:
        color = 'orange'
    elif value <= 55:
        color = 'yellow'
    elif value <= 75:
        color = 'lightgreen'
    else:
        color = 'green'

    import plotly.graph_objects as go

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'font': {'size': 40, 'color': 'black'},
            'prefix': '',
            'suffix': ''
        },
        delta={'reference': 0, 'position': "bottom", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 0, 'tickcolor': "white", 'visible': False},
            'bar': {'color': "white", 'thickness': 0},  # Hidden bar
            'bgcolor': "white",
            'borderwidth': 0,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 25], 'color': 'rgba(255, 0, 0, 0.4)'},      # Red with transparency
                {'range': [25, 50], 'color': 'rgba(255, 165, 0, 0.4)'},   # Orange with transparency
                {'range': [50, 75], 'color': 'rgba(255, 255, 0, 0.4)'},   # Yellow with transparency  
                {'range': [75, 100], 'color': 'rgba(0, 255, 0, 0.4)'}],   # Green with transparency
            'threshold': {
                'line': {'color': "black", 'width': 3},
                'thickness': 0.8,
                'value': value
            }
        }
    ))

# Add titles to replicate alternative.me layout
    fig.update_layout(
        title={
            'text': "Fear & Greed Index",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': 'black'}
        },
        margin=dict(t=100, b=50, l=50, r=50),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': "black", 'family': "Arial"}
    )

# Add the "Now" caption above the value
    fig.add_annotation(
        text=f"Now: {value}",
        x=0.5,
        y=0.3,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={'size': 18, 'color': 'black'}
    )

# Add the horizontal line
    fig.add_shape(
        type="line",
        x0=0.25, y0=0.45,
        x1=0.75, y1=0.45,
        line=dict(color="black", width=2),
        xref="paper",
        yref="paper"
    )

    return fig

def get_fear_greed_sentiment(value):
    """Convert numeric value """
    if value <= 25:
        return "Extreme Fear"
    elif value <= 45:
        return 'Fear'
    elif value <= 55:
        return "Neutral"
    elif value <= 74:
        return 'Greed'
    else:
        return 'Extreme Greed'

def main():
    with st.sidebar:
        st.title('Fear & Greed Index Dashboard:')
        st.write("")
        st.write("")
        st.write("Should you follow the Index?")
    
    col = st.columns((1.5, 4.5, 2), gap='medium')

    with col[0]:
        df = load_data()
        latest = df.iloc[-1]
        current_date = latest['date_index'].strftime('%B, %d')

        #extract values
        fg_index_num = latest.get('fg_index_num')
        fg_index_str = latest.get('fg_index_str')
        gauge_fig = create_gauge_chart(fg_index_num, 'Fear & Greed Index')
        st.plotly_chart(gauge_fig, use_container_width=True)
    

if __name__=='__main__':
    main()