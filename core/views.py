from django.shortcuts import render
from .models import PetroleumDetails
from django.db.models import Count,Sum,Avg,Value,CharField
from django.views.generic import View, ListView
import requests
import itertools
from django.db import connection
import json
# Create your views here.
class IndexView(ListView):
    model = PetroleumDetails
    template_name = 'index.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        r = requests.get('https://raw.githubusercontent.com/younginnovations/internship-challenges/master/programming/petroleum-report/data.json')
        records = json.loads(r.content.decode('utf-8'))
        print("records",records)
        #We define two lists:
        # one list for holding the values that we want to insert
        # records list may contains the values that would have been updated as well so we have distinguished the records to insert and update separately
        # another list for the new values if data.json had updated values or contains any new values
        records_to_create = []
        records_to_update = []
        
        # This is where we check if the records are pre-existing,
        # and add primary keys to the objects if they do

        records = [
            {
                "id": PetroleumDetails.objects.filter(
                    year = record['year'],
                    petroleum_product = record['petroleum_product'],
                    sale = record['sale'],
                    country = record['country'],
                ).first().id

                if PetroleumDetails.objects.filter(
                    year = record['year'],
                    petroleum_product = record['petroleum_product'],
                    sale = record['sale'],
                    country = record['country'],
                    ).first() is not None
                else None,
                **record,
            }
            for record in records
        ]
        
        # This is where we separate our records to our split lists: 
        # - if the record already exists in the sqlite database (the 'id' primary key), add it to the update list.
        # - else add it to the create list.
        [
            records_to_update.append(record)
            if record["id"] is not None
            else records_to_create.append(record)
            for record in records
        ]
        
        # Remove the 'id' field, as these will all hold a value of None for records to create,
		# since these records do not already exist in the DB
        [record.pop("id") for record in records_to_create]
        
        #using bulk_create and bulk_update so as all the operation happens in single statement
        created_records = PetroleumDetails.objects.bulk_create(
            [PetroleumDetails(**values) for values in records_to_create], batch_size=500
        )
        PetroleumDetails.objects.bulk_update(
            [
                PetroleumDetails(id=values.get("id"), year = values['year'],
                petroleum_product = values['petroleum_product'],
                sale = values['sale'],
                country = values['country'])
                for values in records_to_update
            ],
            ["year","petroleum_product","sale","country"],
            batch_size=500
        )
        petroleum_details = PetroleumDetails.objects.all()
        context['all_petroleum'] = petroleum_details
        return context


class TotalSalesView(ListView):
    model = PetroleumDetails
    template_name = 'total_sales.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        total_sales = []
        #annotating the sale__sum along with the petroleum product values
        sales = PetroleumDetails.objects.values('petroleum_product').annotate(Sum('sale'))
        print(sales)
        context['sales'] = sales
        return context 

class ByCountryView(ListView):
    model = PetroleumDetails
    template_name = 'country.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        #annotating the sale__sum based on the value country of our model
        #and ordering in descending/ascending order of total sale sum and slicing the first 3 records only
        high_country = PetroleumDetails.objects.values('country').annotate(Sum('sale')).order_by('-sale__sum')
        low_country = high_country.reverse()
        context['high_country'] = high_country[:3]
        context['low_country'] = low_country[:3]
        return context


def my_custom_sql(year1,year2):
    with connection.cursor() as cursor:
        cursor.execute('SELECT sale,year,petroleum_product from core_petroleumdetails where year between "'+str(year1)+'" and "'+str(year2)+'"')
        row = cursor.fetchall()

    return row

class AverageSalesView(ListView):
    model = PetroleumDetails
    template_name = 'average.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        #obtaining two different querysets for the year range 2007-2010 and 2011-2014 respectively
        avg_data1 = PetroleumDetails.objects.values('petroleum_product').exclude(sale = 0).filter(year__range=(2007,2010)).annotate(avg_sale = Avg('sale')).annotate(year_range = Value('2007-2010',output_field=CharField()))
        avg_data2 = PetroleumDetails.objects.values('petroleum_product').exclude(sale = 0).filter(year__range=(2011,2014)).annotate(avg_sale = Avg('sale')).annotate(year_range = Value('2011-2014',output_field=CharField()))
        #creating the final list that contains the alternating element from avg_data1 and avg_data2
        final_data = [x for x in itertools.chain.from_iterable(itertools.zip_longest(avg_data1,avg_data2)) if x]
        context['final_data'] = final_data
        return context


