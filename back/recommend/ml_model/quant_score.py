# recommend/ml_model/quant_score.py

def calculate_quant_score(row):
    """
    간단한 퀀트 점수 계산 예시 (0 ~ 4점)
    - PER이 낮을수록
    - ROE가 높을수록
    - RSI가 30~70이면 중립, 벗어나면 감점
    - SMA20_diff가 양수면 가산
    """
    score = 0

    # PER (저평가일수록 좋음)
    if row['PER'] is not None and row['PER'] < 15:
        score += 1

    # ROE (높을수록 좋음)
    if row['ROE'] is not None and row['ROE'] > 0.15:
        score += 1

    # RSI (중립 범위가 이상적)
    if row['RSI'] is not None and 30 <= row['RSI'] <= 70:
        score += 1

    # SMA20_diff (이동평균 위에 있으면 긍정)
    if row['SMA20_diff'] is not None and row['SMA20_diff'] > 0:
        score += 1

    return score
