from pfinder.models import Place, PlaceToken
from django.contrib.gis import admin as admin

admin.site.register(Place, admin.GeoModelAdmin)
admin.site.register(PlaceToken)
