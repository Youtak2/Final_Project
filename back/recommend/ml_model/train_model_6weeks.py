import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAST_CSV = os.path.join(BASE_DIR, 'training_data_6weeks_ago_cleaned.csv')
CURR_CSV = os.path.join(BASE_DIR, 'training_data_cleaned.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model_6weeks_ago.pkl')

# 데이터 로드
df_past = pd.read_csv(PAST_CSV)
df_curr = pd.read_csv(CURR_CSV)[['symbol', 'target']]

# 두 데이터 조인 (inner join으로 동일 종목만)
df_merged = pd.merge(df_past, df_curr, on='symbol', how='inner')

# 특성(X)과 타겟(y) 준비
X = df_merged[['PER', 'ROE', 'SMA20_diff', 'RSI']]
y = df_merged['target']

# 결측 제거
mask = X.notnull().all(axis=1)
X = X.loc[mask]
y = y.loc[mask]

# 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 모델 저장
joblib.dump(model, MODEL_PATH)
print(f"✅ 모델 저장 완료: {MODEL_PATH}")
