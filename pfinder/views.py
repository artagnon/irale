from models import Place, PlaceToken
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
from django.contrib.gis.measure import D
import json
import geojson

def placeToJSONFeature(p):
    props=dict([(i.key, i.value) for i in
                (PlaceToken.objects.filter(place=p.id))])
    props['name'] = p.name
    feature=geojson.Feature(p.id,
                            geojson.geometry.Point(p.location.coords),
                            props)
    return feature

def placeListToFeatureCollection(placeList):
    return geojson.feature.FeatureCollection(
        [placeToJSONFeature(i) for i in placeList])

def lookupId(request, pid):
    try:
        this_place = Place.objects.get(id = pid)
        dispatch = placeToJSONFeature(this_place)
        return HttpResponse(geojson.dumps(dispatch), content_type = 'application/json')
    except Exception as e:

        return HttpResponseBadRequest('Place missing' + str(e))

def lookupKey(request, key):
    dispatch = placeListToFeatureCollection(Place.objects.filter(placetoken__key = key))
    return HttpResponse(geojson.dumps(dispatch), content_type = 'application/json')

def lookupToken(request, key, value):
    dispatch = placeListToFeatureCollection(
        Place.objects.filter(placetoken__key = key, placetoken__value = value))
    return HttpResponse(geojson.dumps(dispatch), content_type = 'application/json')

def lookupBounds(request):
    nwpoint = request.GET.get('nw')
    sepoint = request.GET.get('se')
    if nwpoint.find(',') < 0 or sepoint.find(',') < 0:
        return HttpResponseBadRequest('Malformed coordinates')
    xmin, ymax = [float(x) for x in nwpoint.split(',')]
    xmax, ymin = [float(x) for x in sepoint.split(',')]
    bbox = (xmin, ymin, xmax, ymax)
    dispatch = placeListToFeatureCollection(
        Place.objects.filter(location__contained = Polygon.from_bbox(bbox)))
    return HttpResponse(geojson.dumps(dispatch), content_type = 'application/json')

def lookupAround(request):
    center = request.GET.get('center')
    radius = request.GET.get('radius')
    if center.find(',') < 0:
        return HttpResponseBadRequest('Malformed center coordinates')
    centerx, centery = [float(x) for x in center.split(',')]

    dispatch = placeListToFeatureCollection(
        Place.objects.filter(location__distance_lt=(Point(centerx, centery),
                                                    D(m=radius))))

    return HttpResponse(geojson.dumps(dispatch), content_type = 'application/json')

def createNew(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        thisx, thisy = payload.get('location', None).split(',')
        pnt = GEOSGeometry('POINT(%s %s)' % (thisx, thisy))
        this_place = Place(name = payload.get('name', None), location = pnt)
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
