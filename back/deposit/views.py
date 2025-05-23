from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DepositProduct
from collections import defaultdict
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

class DepositProductListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        queryset = DepositProduct.objects.all()

        product_type = request.query_params.get('productType')
        banks = request.query_params.getlist('bank')
        period = request.query_params.get('period')

        if product_type:
            queryset = queryset.filter(product_type=product_type)
        if banks:
            banks = [b for b in banks if b]
            if banks:
                queryset = queryset.filter(bank_name__in=banks)
        if period:
            queryset = queryset.filter(save_term=int(period))

        # 정제된 응답 형식
        grouped = defaultdict(lambda: {
            "disclosure_month": "2024년 11월",
            "bank_name": "",
            "name": "",
            "rate_6": None,
            "rate_12": None,
            "rate_24": None,
            "rate_36": None
        })

        for item in queryset:
            key = f"{item.bank_name}:{item.name}"
            grouped[key]["disclosure_month"] = item.created_at.strftime("%Y년 %m월")  # ✅ 여기 수정
            grouped[key]["bank_name"] = item.bank_name
            grouped[key]["name"] = item.name
            grouped[key][f"rate_{item.save_term}"] = item.rate


        return Response(list(grouped.values()))
