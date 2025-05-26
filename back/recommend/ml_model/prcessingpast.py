import pandas as pd
import os

# 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(current_dir, 'training_data_6weeks_ago.csv')
output_path = os.path.join(current_dir, 'training_data_6weeks_ago_cleaned.csv')

# CSV 파일 불러오기
df = pd.read_csv(input_path)

# 결측치 처리
df = df.dropna(subset=['symbol'])  # target 컬럼 없으면 빼기
for col in ['PER', 'ROE', 'SMA20_diff', 'RSI']:
    if col in df.columns:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)

# 결과 저장
df.to_csv(output_path, index=False)
print(f"✅ 6주전 데이터 전처리 완료: {output_path}")
print(f"📊 남은 데이터 수: {len(df)}개")
print(f"❓ 컬럼별 결측값:\n{df.isnull().sum()}")
