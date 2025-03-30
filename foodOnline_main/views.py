from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def home(request):
    if 'lat' in request.GET:
        lat = request.objects.GET('lat')
        lng = request.objects.GET('lng')
        pnt = GEOSGeometry("POINT(%s %s)" % (lng, lat), srid=4326)
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=100))).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

        for v in vendors:
            v.kms = round(v.distance.km, 1)
        print("lat is there")
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
        print("no lat is there")
    context = {
        'vendors': vendors
    }
    return render(request, 'home.html', context)