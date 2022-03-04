
from core.models import PetroleumDetails
from rest_framework import serializers

class PetroleumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetroleumDetails
        fields = ['id','year','sale','petroleum_product','country']

