from django.contrib.auth.models import Group
from .models import *
from django.db.models import Count, F, Value, Q, Avg
from foodapp.settings import MAX_DISTANCE

def is_store_owner(user):
    return Group.objects.get(name="StoreOwners") in user.groups.all()

def create_pending_store(user):
    try:
        return user.store
    except:
        user_location = user.profile.location
        new_location = Location.objects.create(address=user_location.address,country=user_location.country,
                                               region=user_location.region,
                                               subregion_1=user_location.subregion_1,subregion_2=user_location.subregion_2,
                                                lat = user_location.lat,lng = user_location.lng)
        slug = user.username + "-" + "store"

        new_store = Store.objects.create(user = user,location=new_location,
                                         status = Store_Status.objects.get(code="pending"),slug = slug)
        return new_store

def  recommended_stores(request):
    user = request.user
    if user.is_anonymous:
        return Store.objects.filter(status__code="active")

    else:
        if user.profile.current_order != None:
            current_location = user.profile.current_order.destination
        else:
            current_location = user.profile.location

        stores = Store.objects.all().exclude(user=user) \
            .filter(status__code="active") \
            .annotate(distance=(((F("location__lat") - current_location.lat) ** 2.
                                 + (F("location__lng") - current_location.lng) ** 2.)
                                ** 0.5 * 111.319)) \
            .filter(distance__lte=2 * MAX_DISTANCE)
        for s in stores:
            s.distance = round(s.distance, ndigits=2)

        return stores