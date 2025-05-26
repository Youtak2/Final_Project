import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewsArticle

# ✅ Gemini 설정
genai.configure(api_key="AIzaSyAMYo5qfBsIjcFV8o1KU3Y77Ln-S8GGsss")
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# ✅ 1. RSS 기반 뉴스 수집
def crawl_news(request):
    symbol = request.GET.get("symbol", "").upper()
    if not symbol:
        return JsonResponse({"error": "symbol 파라미터가 필요합니다."}, status=400)

    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(rss_url, headers=headers, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, features="xml")
    except Exception as e:
        return JsonResponse({"error": f"RSS 요청 실패: {e}"}, status=500)

    items = soup.find_all("item")
    print(f"📰 RSS 기사 개수: {len(items)}")
    count = 0

    for item in items:
        try:
            title = item.title.text
            link = item.link.text
            description = item.description.text
            source = item.source.text if item.source else "Yahoo Finance"

            if not NewsArticle.objects.filter(link=link).exists():
                NewsArticle.objects.create(
                    symbol=symbol,
                    title=title,
                    source=source,
                    link=link,
                    content=description
                )
                count += 1
        except Exception as e:
            print("[ERROR] RSS 파싱 실패:", e)
            continue

    return JsonResponse({"message": f"{symbol} 뉴스 수집 완료 (RSS)", "저장된 기사 수": count})

# ✅ 2. Gemini 기반 요약 및 감성 분석
@csrf_exempt
def summarize_news(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)

    try:
        body = json.loads(request.body)
        symbol = body.get("symbol", "").upper()
        if not symbol:
            return JsonResponse({"error": "symbol 파라미터가 필요합니다."}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON 파싱 실패"}, status=400)

    articles = NewsArticle.objects.filter(symbol=symbol).filter(
        translated_summary__isnull=True
    ) | NewsArticle.objects.filter(
        symbol=symbol, translated_summary__startswith="⚠️"
    )

    if not articles.exists():
        return JsonResponse({"message": "요약할 뉴스가 없습니다."})

    count = 0
    for article in articles:
        try:
            prompt = f"""
다음은 투자 관련 뉴스 요약입니다:
\"\"\"
{article.content[:500]}
\"\"\"

1. 위 내용을 한국어로 자연스럽게 번역하세요.
2. 이 뉴스가 투자자에게 긍정, 부정, 중립 중 하나로 감성 분석 결과를 명확히 말해주세요.
"""
            response = model.generate_content(prompt)
            content = response.text.strip()
            print("🧠 Gemini 응답 결과:", content)

            # 감성 분석 결과 추출
            match = re.search(r"(긍정|부정|중립)", content)
            if match:
                article.impact = match.group(1)
            else:
                article.impact = "기타"

            # 번역된 요약 추출
            if "1." in content and "2." in content:
                translated, _ = content.split("2.", 1)
                article.translated_summary = translated.replace("1.", "").strip()
            else:
                article.translated_summary = content
                article.impact = "기타"

            article.save()
            count += 1

        except Exception as e:
            print("[ERROR] Gemini 요약 실패:", e)
            article.translated_summary = f"⚠️ 요약 실패: {str(e)}"
            article.impact = "오류"
            article.save()
            continue

    return JsonResponse({"message": "요약 완료", "요약된 기사 수": count})

# ✅ 3. 요약된 기사 결과 조회
def summarized_results(request):
    symbol = request.GET.get("symbol", "").upper()
    if not symbol:
        return JsonResponse({"error": "symbol 파라미터가 필요합니다."}, status=400)

    articles = NewsArticle.objects.filter(symbol=symbol, translated_summary__isnull=False)
    results = [
        {
            "title": a.title,
            "source": a.source,
            "translated_summary": a.translated_summary,
            "impact": a.impact,
            "link": a.link,
        }
        for a in articles
    ]
    return JsonResponse({"results": results})
