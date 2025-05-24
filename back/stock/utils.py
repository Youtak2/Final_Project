# stock/utils.py

import requests
import datetime
import pandas as pd
from .models import PriceData
from django.db import OperationalError

def get_yahoo_price_data(ticker, days=30):
    end = int(datetime.datetime.now().timestamp())
    start = int((datetime.datetime.now() - datetime.timedelta(days=days)).timestamp())
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={start}&period2={end}&interval=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ 요청 실패:", response.status_code)
        return pd.DataFrame()

    try:
        data = response.json()
        timestamps = data['chart']['result'][0]['timestamp']
        quotes = data['chart']['result'][0]['indicators']['quote'][0]
        df = pd.DataFrame(quotes)
        df['date'] = pd.to_datetime(timestamps, unit='s')
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        return df
    except Exception as e:
        print("❌ JSON 파싱 실패:", e)
        return pd.DataFrame()


def save_to_db(df, ticker):
    for _, row in df.iterrows():
        try:
            PriceData.objects.update_or_create(
                ticker=ticker,
                date=row['date'].date(),
                defaults={
                    'open': row['open'],
                    'high': row['high'],
                    'low': row['low'],
                    'close': row['close'],
                    'volume': row['volume']
                }
            )
        except OperationalError as e:
            print(f"❌ DB 접근 오류: {e}")