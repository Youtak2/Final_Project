import yfinance as yf
import requests
import json
import time

# ✅ DeepL API 키 입력
DEEPL_API_KEY = "b11f45f5-c985-4551-a7a9-4f8d7eb8363a:fx"

# ✅ 번역할 종목 티커 (대표 1~2개로 충분)
TICKERS = ["AAPL", "MSFT", "GOOGL"]

# ✅ 모든 항목을 저장할 집합
term_set = set()

# ✅ 1. 모든 종목의 손익계산서, 대차대조표, 현금흐름표 항목 추출
for symbol in TICKERS:
    ticker = yf.Ticker(symbol)
    for df in [ticker.financials, ticker.balance_sheet, ticker.cashflow]:
        if df is not None and not df.empty:
            df.columns = df.columns.astype(str)
            term_set.update(df.index.tolist())

print(f"📌 총 추출된 항목 수: {len(term_set)}")

# ✅ 2. DeepL API로 영어 → 한국어 번역
translations = {}
for i, term in enumerate(term_set):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": term,
        "source_lang": "EN",
        "target_lang": "KO"
    }

    res = requests.post(url, data=params)
    if res.status_code == 200:
        translated = res.json()["translations"][0]["text"]
        translations[term] = translated
        print(f"{i+1}. ✅ {term} → {translated}")
    else:
        print(f"{i+1}. ❌ 오류 발생: {res.status_code} - {res.text}")
    
    time.sleep(0.5)  # API 연속 호출 제한 대응

# ✅ 3. JSON 저장
with open("korean_labels.json", "w", encoding="utf-8") as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print("✅ 변환 완료! korean_labels.json 저장됨 🎉")
