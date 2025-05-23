from django.contrib import admin
from .models import DepositProduct

# Register your models here.

@admin.register(DepositProduct)
class DepositProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank_name', 'product_type', 'save_term', 'rate')
    list_filter = ('product_type', 'bank_name', 'save_term')
    search_fields = ('name',)