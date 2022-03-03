from django.urls import path
from .views import IndexView,TotalSalesView,ByCountryView,AverageSalesView

app_name = "core"

urlpatterns = [
    path('',IndexView.as_view(),name='home'),
    path('total_sales/',TotalSalesView.as_view(),name='total-sales'),
    path('filter_by_country/',ByCountryView.as_view(),name='filter-by-country'),
    path('average_sales/',AverageSalesView.as_view(),name='average-sales'),
]