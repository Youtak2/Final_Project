from django.urls import path
from .views import crawl_news, summarize_news, summarized_results, sentiment_stats

urlpatterns = [
    path('crawl/', crawl_news),                   # GET /api/v1/news/crawl/?symbol=AAPL
    path('summarize/', summarize_news),           # POST /api/v1/news/summarize/
    path('result/', summarized_results),          # GET /api/v1/news/result/?symbol=AAPL
    path('sentiment-stats/', sentiment_stats),
]