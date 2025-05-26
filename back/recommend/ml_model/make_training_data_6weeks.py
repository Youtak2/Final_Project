# make_training_data_6weeks.py

import os
import json
import pandas as pd
import yfinance as yf
from features import compute_rsi  # 같은 디렉토리에 있어야 함


def fetch_features_6weeks_ago(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period='3mo')

        if hist.empty or len(hist) < 35:
            print(f"⚠️ {symbol} → 데이터 부족 (len={len(hist)})")
            return None

        close = hist['Close']
        idx = -30
        sma20 = close.rolling(20).mean().iloc[idx]
        sma_diff = (close.iloc[idx] - sma20) / sma20 if sma20 else None
        rsi = compute_rsi(close[:idx + 1])

        return {
            'symbol': symbol,
            'PER': info.get('trailingPE'),
            'ROE': info.get('returnOnEquity'),
            'SMA20_diff': sma_diff,
            'RSI': rsi,
        }

    except Exception as e:
        print(f"⚠️ {symbol} 오류: {e}")
        return None


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TICKERS_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..', 'front', 'src', 'assets', 'tickers.json'))
    OUTPUT_PATH = os.path.join(BASE_DIR, 'training_data_6weeks_ago.csv')

    if not os.path.exists(TICKERS_PATH):
        raise FileNotFoundError(f"❌ tickers.json 파일이 존재하지 않습니다: {TICKERS_PATH}")

    with open(TICKERS_PATH, encoding='utf-8') as f:
        tickers = json.load(f)


    rows = []
    for i, item in enumerate(tickers, 1):
        symbol = item['symbol']
        print(f"🔄 ({i}/{len(tickers)}) {symbol} 처리 중...")
        row = fetch_features_6weeks_ago(symbol)
        if row:
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ 저장 완료: {OUTPUT_PATH} (총 {len(df)}개 종목)")


if __name__ == '__main__':
    main()
