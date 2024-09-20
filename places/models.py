from django.db import models


class Place(models.Model):
    image_path = models.CharField(null=False)
    image_alt_text = models.CharField(null=False, default='product image')
    image_url = models.CharField(null=True)
    description_eng = models.TextField(null=True)
    name_eng = models.CharField(null=True)
    url = models.CharField(null=True)
    description_fin = models. TextField(null=True)
    name_fin = models.CharField(null=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    postal_code = models.IntegerField(null=False)
    street_name = models.CharField(null=False)
    city = models.CharField(null=False)
    available_time = models.CharField(null=False)
    price = models.CharField(null=False)
