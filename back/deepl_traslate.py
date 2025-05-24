import requests
import json
import time

# 여기에 발급받은 DeepL API 키
DEEPL_API_KEY = "BTUSwRUm4qKfP45Bg"

financial_terms = [
    "Net Income", "Total Revenue", "Operating Income", "EBITDA",
    "Gross Profit", "Interest Expense", "Research And Development",
    "Long Term Debt", "Inventory", "Basic EPS"
    # 추후 더 추가 가능
]

translations = {}

for term in financial_terms:
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": term,
        "source_lang": "EN",
        "target_lang": "KO"
    }

    res = requests.post(url, data=params)
    if res.status_code == 200:
        result = res.json()
        translated = result["translations"][0]["text"]
        translations[term] = translated
        print(f"✅ {term} → {translated}")
    else:
        print(f"❌ Error: {res.text}")

    time.sleep(0.5)  # 호출 제한 대응

# 결과 저장
with open("korean_labels.json", "w", encoding="utf-8") as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print("📦 번역 완료 → korean_labels.json")
