from pfinder.models import Place, PlaceToken
from django.contrib import admin
from django.contrib.gis import admin as gisadmin

gisadmin.site.register(Place, gisadmin.GeoModelAdmin)
admin.site.register(PlaceToken)
