import sys
sys.path.append('../src')

import pandas as pd
import requests
from datetime import datetime
from constants import bitcoin_url, hashrate_url

def bitcoin():
    response = pd.DataFrame(requests.get(bitcoin_url).json())
    raw_data = []
    for point in response['prices']:
        timestamp = pd.to_datetime(point[0], unit='ms')
        price = point[1]
        raw_data.append({
            'date': timestamp.date(),
            'btc_price': price
        })
    df = pd.DataFrame(raw_data)
    return df

def hashrate():
    url = hashrate_url
    response = pd.DataFrame(requests.get(url).json())
    hashrate_data = []
    for idx, row in response.iterrows():
        timestamp = row['hashrate_value']['x']
        hashrate_value = row['hashrate_value']['y']
        hashrate_data.append({
            'timestamp': timestamp,
            'hashrate_value': hashrate_value
        })
    df = pd.DataFrame(hashrate_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df = df.drop(columns='timestamp')
    df = df.sort_values('date').reset_index(drop = True)
    return df

def merge_hash_btc(hash, btc):
    btc = bitcoin()
    hash = hashrate()
    df = pd.merge(btc, hash, on = 'date', how='left')
    df = df.dropna()
    return df