# irale

Backend for a generic place-finding application using PostGIS and
GeoDjango.

## API endpoints

^id/(\d+)/$ - search by id.  Returns a GeoJSON Feature.

^search/(\w+)/$ - search by key.  Returns a GeoJSON FeatureCollection.

^search/(?P<key>\w+)/(?P<value>\w+)/$ - search by key and value.
Returns a GeoJSON FeatureCollection.

^bounds/$ - search by bounding box; uses GET parameters like: ?nw=
23,34.4&se=239,51.  Returns a GeoJSON FeatureCollection.

^around/$ - search by proximity to coordinate; uses GET parameters
like: ?center=39.2,21&radius=200 (where radius is in meters).  Returns
a GeoJSON FeatureCollection.

^new/$ - add a new place; POST a JSON like this to it: {"name":
"boar"}.  Returns status code.

^edit/(\d+)/$ - edit an existing place by id.  POST a JSON like this
to it: {"name": "quire", "key": "type", "value": "bar"}.  Returns
status code.

^attach/(\d+)/$ - add a key/ value pair to an existing place by id.
POST a JSON like this to it: {"key": "near", "value": "beach"}.
Returns status code.

## GeoJSON data format

All responses are returned in this format.

A GeoJSON Feature looks like:

    {
        "type": "Feature",
        "properties": {
            "name": "Coors Field",
            "amenity": "Baseball Stadium",
            "popupContent": "This is where the Rockies play!"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-104.99404, 39.75621]
        }
    }

A GeoJSON FeatureCollection looks like:

    {
        "type": "Feature",
        "properties": {
            "name": "Coors Field",
            "show_on_map": true
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-104.99404, 39.75621]
        }
    }
