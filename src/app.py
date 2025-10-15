import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from matplotlib.colors import LinearSegmentedColormap
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

#create gradient gauge
def create_gradient_gauge(value, max_value = 100, title = 'Fear & Greed Index', cmap_name='RdYlGn'):
    fig, ax = plt.subplots(figsize=(3,3), subplot_kw={'projection': 'polar'})
    start_angle_deg = -135
    end_angle_deg = 135
    total_angle_deg = end_angle_deg - start_angle_deg

    start_angle_rad = np.deg2rad(start_angle_deg)
    end_angle_rad = np.deg2rad(end_angle_deg)
    total_angle_rad = end_angle_rad - start_angle_rad

    cmap = plt.get_cmap(cmap_name)

    num_segments = 200
    segment_angle_rad = total_angle_rad / num_segments

    for i in range(num_segments):
        seg_start_rad = start_angle_rad + i * segment_angle_rad
        seg_end_rad = seg_start_rad + segment_angle_rad
        color_val = i / num_segments
        color = cmap(color_val)
        wedge = Wedge((0, 0), 1, np.rad2deg(seg_start_rad), np.rad2deg(seg_end_rad), width=0.4, facecolor = color, edgecolor = 'none')
        ax.add_patch(wedge)
    
    normalized_value = value/max_value
    needle_angle_rad = start_angle_rad + normalized_value * total_angle_rad

    ax.plot([needle_angle_rad, needle_angle_rad], [0, 0.7], color='black', linewidth = 3, zorder=3)

    center_circle = Circle((0, 0), 0.1, facecolor = 'white', edgecolor = 'black', zorder=4)
    ax.add_patch(center_circle)
    
    ax.text(0, -0.15, f"{value:.1f}", ha = 'center', va='center', fontsize=10, weight='bold', color='black', zorder = 5)

    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")

    ax.set_rticks([])
    ax.set_xticks(np.linspace(start_angle_rad, end_angle_rad, 5))
    ax.set_xticklabels(['0', '25', '50', '75', '100'], fontsize=8)
    ax.set_ylim(0, 1.2)
    ax.set_frame_on(False)
    ax.set_title(title, va='bottom', fontsize=12, pad = 20)
    plt.tight_layout()
    
    return fig

def main():
    st.title('Check Fear & Greed Index')

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig = create_gradient_gauge(42, max_value=100, title='Fear & Greed Index', cmap_name='RdYlGn')
        st.pyplot(fig)

if __name__=='__main__':
    main()