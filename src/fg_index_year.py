import sys
sys.path.append('../src')
from constants import fg_year_url

import requests
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import Union

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_fg_index_year(
    url: str,
    timeout: int = 10,
    format: str = 'json',
    limit: int = 180
) -> Union[pd.DataFrame, None]:
    """
    Return pd.DataFrame of Fear & Greed index during a year
    """
    url = url.format(format=format, limit=limit)
    try:
        response = requests.get(url, timeout=timeout).json()
        df_list = response['data']
        df = pd.DataFrame(df_list)
        df['timestamp'] = pd.to_numeric(df['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.date

        df = df.rename(columns={'value': 'fg_index_num',
                                'value_classification': 'fg_index_str',
                                'timestamp': 'index_date'
                                })
        df = df[['fg_index_num', 'fg_index_str', 'index_date']]
        return df
    except requests.exceptions.RequestException as e:
        logger.error("Error getting Fear & Greed data: %s", e)
        return None