from django.urls import path,re_path,include

from .views import TotalSalesView

urlpatterns = [
    re_path('sales_per_product/',TotalSalesView.as_view({'get':'list'}),name = 'total-sales-per-product'),
]