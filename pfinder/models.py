from django.db import models
from django.contrib.gis.db import models

class Place(models.Model):
    name = models.CharField(max_length=255)

    mpoint = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class PlaceToken(models.Model):
    place = models.ForeignKey('Place')

    key = models.CharField(max_length=255)
    value = models.CharField(max_length=1024)
