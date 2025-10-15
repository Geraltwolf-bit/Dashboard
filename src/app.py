import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

#configure the page
st.set_page_config(
    page_title='Check Fear & Greed Dashboard',
    layout='wide',
    page_icon=':memo:'
)

#connect to the database
@st.cache_resource
def get_database_connection():
    database_url = 'postgresql+psycopg2://admin:admin@localhost:5432/Dashboard'
    return create_engine(database_url)

#loat the data from the database
def load_data():
    engine = get_database_connection()
    query = 'SELECT * FROM fear_greed_index ORDER BY date_index ASC'
    df = pd.read_sql(query, engine)
    return df
