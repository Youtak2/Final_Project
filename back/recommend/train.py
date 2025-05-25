# recommend/ml_model/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv('training_data.csv')  # 수익률에 따라 label (1=상승, 0=하락)

X = df[['PER', 'ROE', 'SMA20_diff', 'RSI']]
y = df['target']  # 1=상승, 0=하락

model = RandomForestClassifier(n_estimators=100)
model.fit(X.dropna(), y.loc[X.dropna().index])

joblib.dump(model, 'recommend/ml_model/model.pkl')
