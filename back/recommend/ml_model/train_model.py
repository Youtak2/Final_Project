import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 데이터 불러오기
df = pd.read_csv('recommend/ml_model/training_data.csv')

X = df[['PER', 'ROE', 'SMA20_diff', 'RSI']]
y = df['target']

# 결측값 제거
X = X.dropna()
y = y.loc[X.index]

# 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 저장
joblib.dump(model, 'recommend/ml_model/model.pkl')
print("✅ model.pkl 저장 완료")
