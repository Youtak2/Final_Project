from rest_framework import serializers
from .models import DepositProduct

class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'
