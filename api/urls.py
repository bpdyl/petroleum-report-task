from django.urls import path,re_path,include

from .views import TotalSalesView,CountrySalesView,AverageSalesAPIView

urlpatterns = [
    re_path('sales_per_product/',TotalSalesView.as_view({'get':'list'}),name = 'total-sales-per-product'),
    re_path('top_sales_per_country/',CountrySalesView.as_view({'get':'list'}),name = 'top-sales-per-country'),
    re_path('average_sales/',AverageSalesAPIView.as_view({'get':'list'}),name = 'average-sales-year-interval'),
]