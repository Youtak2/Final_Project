from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DepositProduct, Bookmark
from collections import defaultdict
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BookmarkSerializer, DepositProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView

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
            grouped[key]["id"] = item.id


        return Response(list(grouped.values()))

class BookmarkToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'No product_id provided'}, status=400)

        product = get_object_or_404(DepositProduct, id=product_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, product=product)

        if not created:
            bookmark.delete()
            return Response({'bookmarked': False})
        return Response({'bookmarked': True})

class BookmarkListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookmarks = Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def related_products(request, product_id):
    try:
        product = DepositProduct.objects.get(pk=product_id)
        same_group = DepositProduct.objects.filter(
            name=product.name,
            bank_name=product.bank_name,
            product_type=product.product_type
        )
        serializer = DepositProductSerializer(same_group, many=True)
        return Response(serializer.data)
    except DepositProduct.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    


class DepositProductDetailView(RetrieveAPIView):
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductSerializer