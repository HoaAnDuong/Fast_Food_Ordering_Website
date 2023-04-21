from django.db import models
# from django.contrib.gis.db.models import PointField
# Create your models here.

class Country(models.Model):
    name = models.TextField(max_length=100,blank=False,default="")

    class Meta:
        db_table = "Country"
        verbose_name = "Country"

    def __str__(self):
        return self.name

class Location(models.Model):
    address = models.TextField(max_length=512,blank=True,default="")
    country = models.TextField(max_length=100,blank=True,default="")
    region = models.TextField(max_length=100,blank=True,default="")
    subregion_1 = models.TextField(max_length=100, blank=True, default="")
    subregion_2 = models.TextField(max_length=100, blank=True, default="")
    # street_name = models.TextField(max_length=255, blank=True, default="")
    lat = models.FloatField(default=16.07387)
    lng = models.FloatField(default=108.14975)

    class Meta:
        db_table = "Location"
        verbose_name = "Location"

    def __str__(self):
        return self.address

