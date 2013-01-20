from models import Place, PlaceToken
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
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
    these_places = list(Place.objects.filter(
        mpoint__contained = Polygon.from_bbox(bbox)))
    dispatch = [{'id': this_place.id, 'name': this_place.name,
                 'x': this_place.mpoint.x, 'y': this_place.mpoint.y}
                for this_place in these_places]
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def lookupAround(request):
    center = request.GET.get('center')
    radius = request.GET.get('radius')
    if center.find(',') < 0:
        return HttpResponseBadRequest('Malformed center coordinates')
    centerx, centery = [float(x) for x in center.split(',')]
    these_places = list(Place.objects.filter(mpoint__distance_lt=(
                Point(centerx, centery), D(m=radius))))
    dispatch = [{'id': this_place.id, 'name': this_place.name,
                 'x': this_place.mpoint.x, 'y': this_place.mpoint.y}
                for this_place in these_places]
    return HttpResponse(json.dumps(dispatch), content_type = 'application/json')

def createNew(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        thisx, thisy = payload.get('mpoint', None).split(',')
        pnt = GEOSGeometry('POINT(%s %s)' % (thisx, thisy))
        this_place = Place(name = payload.get('name', None), mpoint = pnt)
        this_place.save()
        return HttpResponse('Success')
    else:
        return HttpResponseBadRequest('Missing POST data')

def editId(request, pid):
    if request.method == 'POST':
        payload = json.loads(request.body)
        this_place = Place.objects.get(id = pid)
        this_place.name = payload.get('name', None)
        this_token = PlaceToken(place = this_place,
                                key = payload.get('key', None),
                                value = payload.get('value', None))
        this_place.save()
        this_token.save()
        return HttpResponse('Success')
    else:
        return HttpResponseBadRequest('Missing POST data')

def addToken(request, pid):
    if request.method == 'POST':
        payload = json.loads(request.body)
        try:
            this_place = Place.objects.get(id = pid)
            this_token = PlaceToken(place = this_place,
                                    key = payload.get('key', None),
                                    value = payload.get('value', None))
            this_token.save()
            return HttpResponse('Success')
        except:
            return HttpResponseBadRequest('Place missing')
    else:
        return HttpResponseBadRequest('Missing POST data')
