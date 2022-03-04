import itertools
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
    def list(self,request):
        sales = PetroleumDetails.objects.values('petroleum_product').annotate(total_sale = Sum('sale'))
        response = {
            'total_sales_per_product':sales,
        }
        return Response(response,status=200)

class CountrySalesView(viewsets.ModelViewSet):
    serializer_class = PetroleumDetailSerializer
    def list(self,request):
        #annotating the sale__sum based on the value country of our model
        #and ordering in descending/ascending order of total sale sum and slicing the first 3 records only
        high_country = PetroleumDetails.objects.values('country').annotate(Sum('sale')).order_by('-sale__sum')
        low_country = high_country.reverse()
        response = {
            'top_highest_sales_country':high_country[:3],
            'top_lowest_sales_country':low_country[:3],
        }
        return Response(response,status=200)

class AverageSalesAPIView(viewsets.ModelViewSet):
    serializer_class = PetroleumDetailSerializer
    def list(self,request):
        #annotating the sale__sum based on the value country of our model
        #and ordering in descending/ascending order of total sale sum and slicing the first 3 records only
        avg1 = PetroleumDetails.objects.filter(year__range = (2007,2010)).exclude(sale = 0).values('petroleum_product').annotate(avg_sale = Avg('sale')).annotate(year_range = Value('2007-2010',output_field=CharField()))
        avg2 = PetroleumDetails.objects.filter(year__range = (2011,2014)).exclude(sale = 0).values('petroleum_product').annotate(avg_sale = Avg('sale')).annotate(year_range = Value('2011-2014',output_field=CharField()))
        final_average = [x for x in itertools.chain.from_iterable(itertools.zip_longest(avg1,avg2)) if x]
        response = {
            "average_sales":final_average,
        }
        return Response(response,status=200)