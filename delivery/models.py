from django.db import models
from django.contrib.auth.models import User
from locations.models import Location
from locations.utils import distance
from orders.models import Order
import datetime
from django.utils.timezone import make_aware
from django.db.models import Count, F, Value
from foodapp.settings import MAX_DELIVERY_DISTANCE
from django.core.exceptions import ValidationError
from locations.models import Location
from django.db import transaction
# Create your models here.

class Deliverer_Profile_Status(models.Model):
    code = models.CharField(max_length=20)
    def __str__(self):
        return self.code

class Delivery_Status(models.Model):
    code = models.CharField(max_length=20)
    def __str__(self):
        return self.code



class Deliverer_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="deliverer_profile")
    status = models.ForeignKey(Deliverer_Profile_Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    current_location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    driver_license = models.DecimalField(max_digits=12,decimal_places=0,blank=True,null=True)
    moderated = models.DateTimeField(blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.profile.last_name} {self.user.profile.first_name} ({self.user.username})"

    def update_current_location(self,request):
        self.current_location.region = self.user.profile.location.region
        self.current_location.country = self.user.profile.location.country
        self.current_location.lat = request.POST.get('current_lat')
        self.current_location.lng = request.POST.get('current_lng')
        self.last_active = datetime.datetime.now()
        self.current_location.save()
        self.save()
    @property
    def is_active(self):
        return self.status.code == "active" and datetime.datetime.now().date() == self.last_active.date()

    @property
    def name(self):
        return f"{self.user.profile.last_name} {self.user.profile.first_name}"
    @property
    def email(self):
        return self.user.profile.email
    @property
    def phone_number(self):
        return self.user.profile.phone_number

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")
    deliverer = models.ForeignKey(Deliverer_Profile, on_delete=models.CASCADE, related_name='deliveries',
                                  blank=True, null=True)
    start_point = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    total_length = models.FloatField(default=0)
    status = models.ForeignKey(Delivery_Status, on_delete=models.DO_NOTHING, blank=True, null=True)

    def set_start_position(self):
        current_location = self.deliverer.current_location
        if self.start_point:
            self.start_point.country = current_location.country
            self.start_point.region = current_location.region
            self.start_point.lat = current_location.lat
            self.start_point.lng = current_location.lng
        else:
            start_point = Location.objects.create(country=current_location.country, region=current_location.region,
                                                  lat=current_location.lat, lng=current_location.lng)
            self.start_point = start_point
    def find_deliverer(self):
        if self.order.order_status.code != "pending":
            raise ValidationError("Bạn không thể thực hiện thay đổi trên đơn hàng này.")
        shortest_path = self.order.shortest_path()["path"]

        for point in shortest_path:
            deliverers = Deliverer_Profile.objects\
                                                .filter(current_location__region = self.order.destination.region)\
                                                .exclude(user = self.order.customer)\
                                                .annotate(distance = ((F("current_location__lat")-point.lat) ** 2.
                                                    + (F("current_location__lng")-point.lng) ** 2.)
                                                    ** 0.5 * 111.319)\
                                                .filter(distance__lte = MAX_DELIVERY_DISTANCE)\
                                                .order_by('distance')

            if len(deliverers) != 0:
                for chosen_deliverer in deliverers:

                    if chosen_deliverer.is_active and len(chosen_deliverer.deliveries.filter(status__code = "delivering")) == 0:
                        self.deliverer = chosen_deliverer
                        self.save()
                        break
                if self.deliverer != None:
                    self.status = Delivery_Status.objects.get(code = "delivering")
                    self.save()
                    break
        if self.deliverer == None:
            raise ValidationError("Không tìm thấy Người giao hàng.")
        else:
            self.get_route()

    def delete_route(self):
        route = self.points.all().order_by("priority")
        for point in route:
            point.delete()
        self.save()
    def get_route(self):
        self.delete_route()
        self.set_start_position()
        shortest_path = self.order.shortest_path(with_start_pos=True)["path"]
        for i, point in enumerate(shortest_path):
            try:
                with transaction.atomic():
                    self.points.create(priority=i,
                                       location=Location.objects.create(address=point.address,
                                                                        country=point.country,
                                                                        region=point.region,
                                                                        subregion_1=point.subregion_1,
                                                                        subregion_2=point.subregion_2,
                                                                        lat=point.lat, lng=point.lng))
            except:
                self.delete_route()
                self.points.create(priority=i,
                                   location=Location.objects.create(address=point.address,
                                                                    country=point.country,
                                                                    region=point.region,
                                                                    subregion_1=point.subregion_1,
                                                                    subregion_2=point.subregion_2,
                                                                    lat=point.lat, lng=point.lng))
        self.save()


class Delivery_Point(models.Model):
    priority = models.PositiveIntegerField(default=1)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="points", null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ["priority", "location"]