from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from .serializers import PetroleumDetailSerializer
from django.db.models import Count,Sum,Avg,Value,CharField
from core.models import PetroleumDetails
from rest_framework.decorators import action
# Create your views here.

class TotalSalesView(viewsets.ModelViewSet):
    serializer_class = PetroleumDetailSerializer
    # @action(methods=['get'],detail=True)
    def list(self,request):
        sales = PetroleumDetails.objects.values('petroleum_product').annotate(total_sale = Sum('sale'))
        response = {
            'total_sales_per_product':sales,
        }
        return Response(response,status=200)
