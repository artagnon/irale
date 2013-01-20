from models import Place, PlaceToken
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D
import json

def lookupId(request, pid):
    try:
        this_place = Place.objects.get(id = pid)
        dispatch = {'name': this_place.name,
                    'tokens': list(PlaceToken.objects.filter(
                    place_id = pid).values('key', 'value'))}
        return HttpResponse(json.dumps(dispatch), content_type = 'application/json')
    except:
        return HttpResponseBadRequest('Place missing')

def lookupKey(request, key):
    dispatch = list(Place.objects.filter(placetoken__key = key).values('id', 'name'))
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def lookupToken(request, key, value):
    dispatch = list(Place.objects.filter(
        placetoken__key = key, placetoken__value = value).values('id', 'name'))
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def lookupBounds(request):
    nwpoint = request.GET.get('nw')
    sepoint = request.GET.get('se')
    if nwpoint.find(',') < 0 or sepoint.find(',') < 0:
        return HttpResponseBadRequest('Malformed coordinates')
    xmin, ymax = [float(x) for x in nwpoint.split(',')]
    xmax, ymin = [float(x) for x in sepoint.split(',')]
    bbox = (xmin, ymin, xmax, ymax)
    dispatch = list(Place.objects.filter(
        mpoint__bbcontains = Polygon.from_bbox(bbox)).values(
        'id', 'name'))
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def lookupAround(request):
    center = request.GET.get('center')
    radius = request.GET.get('radius')
    if center.find(',') < 0:
        return HttpResponseBadRequest('Malformed center coordinates')
    centerx, centery = [float(x) for x in center.split(',')]
    dispatch = list(Place.objects.filter(mpoint__distance_lt=(
            Point(centerx, centery), D(m=radius))).values('id', 'name'))
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def createNew(request):
    # Incoming json payload
    return 1

def editId(request, id):
    # Incoming json payload
    return 1
