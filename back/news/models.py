from django.db import models

class NewsArticle(models.Model):
    symbol = models.CharField(max_length=10)    # 종목 티커 (예: AAPL)
    title = models.CharField(max_length=300)    # 뉴스 제목
    source = models.CharField(max_length=100)   # 출처
    link = models.URLField(unique=True)         # 뉴스 URL
    content = models.TextField()                # 전체 본문
    translated_summary = models.TextField(null=True, blank=True)    # 요약 및 번역 결과 (null 허용)
    impact = models.CharField(max_length=20, null=True, blank=True) # 감성 분석 결과 (긍정/부정/중립)
    created_at = models.DateTimeField(auto_now_add=True)            # 저장 시각 (자동 생성)

    def __str__(self):
        return f"[{self.symbol}] {self.title[:40]}..."
