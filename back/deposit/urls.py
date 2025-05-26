from django.urls import path
from .views import DepositProductListView, BookmarkToggleView, BookmarkListView, related_products

urlpatterns = [
    path('products/', DepositProductListView.as_view(), name='deposit-products'),
    path('bookmark/', BookmarkToggleView.as_view(), name='bookmark-toggle'),
    path('bookmark/list/', BookmarkListView.as_view(), name='bookmark-list'),
    path('products/<int:product_id>/group/', related_products),
]
