from django.db import models
from django.contrib.auth.models import User
from locations.models import Location
from orders.models import Order
import datetime
from django.utils.timezone import make_aware
# Create your models here.

class Deliverer_Profile_Status(models.Model):
    code = models.CharField(max_length=20)
    def __str__(self):
        return self.code

class Delivery_Status(models.Model):
    code = models.CharField(max_length=20)
    def __str__(self):
        return self.code

class Delivery(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name="delivery")
    deliverer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveries')
    start_point = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)


class Delivery_Point(models.Model):
    priority = models.PositiveIntegerField(default = 1)
    delivery = models.ForeignKey(Delivery,on_delete=models.CASCADE,related_name="points",null=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    class Meta:
        unique_together = ["priority","location"]

class Deliverer_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="deliverer_profile")
    status = models.ForeignKey(Deliverer_Profile_Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    current_location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    driver_license = models.DecimalField(max_digits=12,decimal_places=0,blank=True,null=True)
    moderated = models.DateTimeField(blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def update_current_location(self,request):
        self.current_location.lat = request.POST.get('current_lat')
        self.current_location.lng = request.POST.get('current_lng')
        self.last_active = make_aware(datetime.datetime.now())
        self.current_location.save()
        self.save()
    @property
    def is_active(self):
        return self.status.code == "active" and datetime.datetime.now().date() == self.user.last_login.date()