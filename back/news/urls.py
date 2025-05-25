from django.urls import path
from .views import crawl_news, summarize_news, summarized_results

urlpatterns = [
    path('crawl/', crawl_news),                   # GET /api/v1/news/crawl/?symbol=AAPL
    path('summarize/', summarize_news),           # POST /api/v1/news/summarize/
    path('result/', summarized_results),          # GET /api/v1/news/result/?symbol=AAPL
]