from locations.models import Location
import datetime
from .models import Profile,User_Status
from django.core.exceptions import ValidationError,ObjectDoesNotExist


def validate_birthdate(date):
    str_date = date.split("-")
    int_date = [int(i) for i in str_date]
    birthdate = datetime.datetime(*int_date)
    if birthdate > datetime.datetime.now():
        raise ValidationError("Ngày sinh không thể là ngày sau ngày hôm nay")

def create_profile(user,first_name,last_name,gender_id,birthdate,phone_number,email):
    try:
        profile = Profile.objects.get(user = user)
        return profile
    except ObjectDoesNotExist:
        location = Location.objects.create()
        active_status = User_Status.objects.get(code="active")

        profile = Profile.objects.create(user=user, location=location, first_name = first_name, last_name=last_name, gender_id=gender_id,
                               birthdate = birthdate, phone_number=phone_number, email=email, status=active_status)
        return profile
