from models import PlaceToken
import geojson

def placeToJSONFeature(p):
    props = dict([(i.key, i.value) for i in
                  (PlaceToken.objects.filter(place = p.id))])
    props['name'] = p.name
    feature = geojson.Feature(p.id,
                              geojson.geometry.Point(p.location.coords),
                              props)
    return feature

def placeListToFeatureCollection(placeList):
    return geojson.feature.FeatureCollection(
        [placeToJSONFeature(i) for i in placeList])
