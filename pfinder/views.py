from models import Place, PlaceToken
from django.http import HttpResponse

def lookupId(request, pid):
    # Place.objects.filter(placetoken__key__contains=key)
    return HttpResponse("Will fetch place with id %s." % pid)

def lookupBoundingBox(request):
    return 1

