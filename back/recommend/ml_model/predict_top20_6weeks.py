# 3_predict_top20_6weeks.py
import pandas as pd
import joblib
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'training_data_6weeks_ago.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model_6weeks_ago.pkl')
OUTPUT_PATH = os.path.join(BASE_DIR, 'predicted_top20_6weeks.json')

df = pd.read_csv(CSV_PATH).dropna()
model = joblib.load(MODEL_PATH)

results = []
for _, row in df.iterrows():
    X = pd.DataFrame([[
        row['PER'], row['ROE'], row['SMA20_diff'], row['RSI']
    ]], columns=['PER', 'ROE', 'SMA20_diff', 'RSI'])

    prob = model.predict_proba(X)[0][1] if hasattr(model, "predict_proba") else 0.5
    results.append({'symbol': row['symbol'], 'probability': round(prob, 4)})

top20 = sorted(results, key=lambda x: -x['probability'])[:20]
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(top20, f, indent=2, ensure_ascii=False)

print(f"✅ 6주 전 기준 top20 저장 완료: {OUTPUT_PATH}")
