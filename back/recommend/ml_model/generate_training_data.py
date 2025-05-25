import os
import json
import pandas as pd
import yfinance as yf
from .features import compute_rsi
import time
def fetch_features(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period='3mo')
        if hist.empty:
            return None

        per = info.get('trailingPE')
        roe = info.get('returnOnEquity')
        close = hist['Close']
        sma20 = close.rolling(20).mean().iloc[-1]
        sma_diff = (close.iloc[-1] - sma20) / sma20 if sma20 else None
        rsi = compute_rsi(close)
        target = 1 if close.iloc[-1] > close.iloc[0] else 0

        return {
            'symbol': symbol,
            'PER': per,
            'ROE': roe,
            'SMA20_diff': sma_diff,
            'RSI': rsi,
            'target': target,
        }
    except Exception as e:
        print(f"[⚠️] {symbol} 오류: {e}")
        return None

def main():
    # ✅ 프로젝트 루트에서 tickers.json 경로 탐색
    current_dir = os.path.dirname(os.path.abspath(__file__))      # ml_model
    recommend_dir = os.path.dirname(current_dir)                   # recommend
    back_dir = os.path.dirname(recommend_dir)                      # back
    project_root = os.path.dirname(back_dir)                       # Final_Project

    TICKERS_PATH = os.path.join(project_root, 'front', 'src', 'assets', 'tickers.json')
    print("✅ TICKERS_PATH:", TICKERS_PATH)

    if not os.path.exists(TICKERS_PATH):
        raise FileNotFoundError(f"❌ tickers.json 파일을 찾을 수 없습니다: {TICKERS_PATH}")

    with open(TICKERS_PATH, encoding='utf-8') as f:
        tickers = json.load(f)

    symbols = [item['symbol'] for item in tickers]
    print(f"🔍 총 {len(symbols)}개 종목 처리 시작...")

    rows = []
    for i, symbol in enumerate(symbols, 1):
        print(f"🔄 ({i}/{len(symbols)}) {symbol} 처리 중...")
        result = fetch_features(symbol)
        if result:
            rows.append(result)

    df = pd.DataFrame(rows)
    output_path = os.path.join(current_dir, 'training_data.csv')
    df.to_csv(output_path, index=False)

    print(f"✅ 학습 데이터 저장 완료: {output_path}")
    print(f"📦 총 저장된 데이터: {len(df)}개")
    print(f"❓ ROE 결측값 수: {df['ROE'].isnull().sum()}")

# 진입점
if __name__ == '__main__':
    main()
