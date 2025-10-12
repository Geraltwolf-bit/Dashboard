import psycopg2
from sqlalchemy import create_engine
import pandas as pd

def connect_db():
    """Connect the existing database to the project"""
    return psycopg2.connect(
        host='localhost',
        port='5432',
        database='Dashboard',
        user='admin',
        password='admin',
        connect_timeout=10
    )

def get_db_engine():
    return create_engine('postgresql+psycopg2://admin:admin@localhost:5432/Dashboard')