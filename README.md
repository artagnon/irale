# irale

Backend for a generic place-finding application using PostGIS and
GeoDjango.  API endpoints:

^id/(\d+)/$ - search by id.  Returns {"id": 1, "name": "bar"}

^search/(\w+)/$ - search by key.  Returns [{"id": 3, "name": "foo"},
...]

^search/(?P<key>\w+)/(?P<value>\w+)/$ - search by key and value.
Returns [{"id": 49, "name": "baz"}, ...]

^bounds/$ - search by bounding box; POST a JSON like this to it:
{"nw": "23,34.4", "se": "239,51"}.  Returns [{"id": 8, "name": "quux",
"x": 232.2, "y": 391.1}, ...]

^around/$ - search by proximity to coordinate; POST a JSON like this
to it: {"center": "39.2,21", "radius": "200"} (where radius is in
meters).  Returns [{"id": 21, "name": "burp", "x": 89.2, "y": 91.4},
...]

^new/$ - add a new place; POST a JSON like this to it: {"name":
"boar"}.  Returns status code.

^edit/(\d+)/$ - edit an existing place by id.  POST a JSON like this
to it: {"name": "quire", "key": "type", "value": "bar"}.  Returns
status code.

^attach/(\d+)/$ - add a key/ value pair to an existing place by id.
POST a JSON like this to it: {"key": "near", "value": "beach"}.
Returns status code.
