from .models import *
from locations.models import Location

def create_deliverer_profile(user):
    try:
        return user.deliverer_profile
    except:
        user_location = user.profile.location
        new_location = Location.objects.create(address=user_location.address,country=user_location.country,
                                               region=user_location.region,
                                               subregion_1=user_location.subregion_1,subregion_2=user_location.subregion_2,
                                                lat = user_location.lat,lng = user_location.lng)


        delivery_profile = Deliverer_Profile.objects.create(user = user,current_location=new_location,
                                         status = Deliverer_Profile_Status.objects.get(code="pending"))
        return delivery_profile