import sys
sys.path.append('../src')
from constants import fg_today_url, fg_year_url
from functions import format_timedelta

import requests
import pandas as pd
import logging
from datetime import datetime
from typing import Union

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_df_fg_index_today(
    url: str,
    timeout: int = 10,
    format: str = 'json'
) -> Union[pd.DataFrame, None]:
    """
    Fetch Fear & Greed index and return dataframe with:
    - current date,
    - numerical index in the range 0-100,
    - index (Extreme Fear, Fear, Greed, Extreme Greed),
    - date,
    - time untill update.
    """
    url = url.format(format=format)
    try:
        response = requests.get(url, timeout=timeout).json()
        df_list = response['data']
        df = pd.DataFrame(df_list)

        df['timestamp'] = pd.to_numeric(df['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.date

        df['time_until_update'] = pd.to_numeric(df['time_until_update'])
        df['time_until_update'] = pd.to_timedelta(df['time_until_update'], unit='s')
        df['time_until_update'] = format_timedelta(df['time_until_update'])

        df = df.rename(columns={'value': 'fg_index_num',
                                'value_classification': 'fg_index_str',
                                'timestamp': 'date_index'
                                })
        return df
    except requests.exceptions.RequestException as e:
        logger.error("Error getting Fear & Greed data: %s", e)
        return None