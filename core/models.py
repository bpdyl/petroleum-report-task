from django.db import models

# Create your models here.
class PetroleumDetails(models.Model):
    year = models.CharField(max_length=10,null=True,blank=True)
    petroleum_product = models.CharField(max_length=100,null=True,blank=True)
    sale = models.IntegerField()
    country = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self) -> str:
        return self.petroleum_product