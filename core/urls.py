from django.urls import path
from .views import IndexView,TotalSalesView

app_name = "core"

urlpatterns = [
    path('',IndexView.as_view(),name='home'),
    path('total_sales/',TotalSalesView.as_view(),name='total-sales'),
]