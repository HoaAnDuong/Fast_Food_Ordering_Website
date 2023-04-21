from django.contrib.auth.models import Group
from .models import *

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
