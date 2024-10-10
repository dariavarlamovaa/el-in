from django.db import models


class Place(models.Model):
    image_path = models.ImageField(upload_to='places/images/', null=False)
    image_alt_text = models.CharField(null=False, default='product image')
    image_url = models.URLField(null=True)
    description_eng = models.TextField(null=True)
    name_eng = models.CharField(null=True)
    url = models.CharField(null=True)
    description_fin = models.TextField(null=True)
    name_fin = models.CharField(null=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    postal_code = models.IntegerField(null=False)
    street_name = models.CharField(null=False)
    city = models.CharField(null=False)
    available_time = models.CharField(null=False)
    price = models.CharField(null=False)

    def get_available_description(self):
        return self.description_eng or self.description_fin

    def get_available_name(self):
        return self.name_eng or self.name_fin

    def __str__(self):
        return self.city
