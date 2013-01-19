from models import Place, PlaceToken
from django.http import HttpResponse
import json

def lookupId(request, pid):
    this_place = Place.objects.get(id = pid)
    dispatch = {'name' : this_place.name}
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def lookupKey(request, key):
    dispatch = list(Place.objects.filter(placetoken__key = key).values('id', 'name'))
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def lookupToken(request, key, value):
    dispatch = list(Place.objects.filter(
        placetoken__key = key, placetoken__value = value).values('id', 'name'))
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def createNew(request):
    # Incoming json payload
    return 1

def editId(request, id):
    # Incoming json payload
    return 1
