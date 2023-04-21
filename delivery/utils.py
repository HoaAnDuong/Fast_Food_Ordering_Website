from .models import *
from locations.models import Location

def create_deliverer_profile(user):
    try:
        return user.deliverer_profile
    except:
        user_location = user.profile.location
        new_location = Location.objects.create(country=user_location.country,
                                               region=user_location.region,
                                                lat = user_location.lat,lng = user_location.lng)


        delivery_profile = Deliverer_Profile.objects.create(user = user,current_location=new_location,
                                         status = Deliverer_Profile_Status.objects.get(code="pending"))
        return delivery_profile