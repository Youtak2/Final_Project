from rest_framework import serializers
from .models import DepositProduct, Bookmark

class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'

class BookmarkSerializer(serializers.ModelSerializer):
    product_detail = DepositProductSerializer(source='product', read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'product', 'created_at', 'product_detail']