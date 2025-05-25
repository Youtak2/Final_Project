import yfinance as yf
import pandas as pd

def get_features(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        fin = ticker.financials
        bs = ticker.balance_sheet
        hist = ticker.history(period='3mo')

        # ROE 계산
        roe = None
        if 'Net Income' in fin.index and 'Total Stockholder Equity' in bs.index:
            try:
                roe = fin.loc['Net Income'].iloc[-1] / bs.loc['Total Stockholder Equity'].iloc[-1]
            except Exception as e:
                print(f"⚠️ {symbol} ROE 계산 실패: {e}")
                roe = None

        # ROE 결측값 처리
        if roe is None:
            roe = -1

        per = info.get('trailingPE')
        price = info.get('currentPrice')

        sma20 = hist['Close'].rolling(20).mean().iloc[-1] if not hist.empty else None
        current_price = hist['Close'].iloc[-1] if not hist.empty else None
        sma_diff = current_price - sma20 if sma20 and current_price else None

        rsi = compute_rsi(hist['Close']) if not hist.empty else None

        return {
            'symbol': symbol,
            'PER': per,
            'ROE': roe,
            'SMA20_diff': sma_diff,
            'RSI': rsi
        }
    except Exception as e:
        print(f"❌ {symbol} feature 생성 실패: {e}")
        return None

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]
