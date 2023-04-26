from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from locations.models import Location
from orders.models import Order
from django.contrib.auth.models import Group
from phonenumber_field.validators import validate_international_phonenumber
from django.core.validators import validate_email

from django.core.exceptions import ValidationError

import datetime
# Create your models here.

class User_Status(models.Model):
	code = models.CharField(max_length=20)
	class Meta:
		db_table = "User_Status"
		verbose_name = "User_Status"

	def __str__(self):
		return self.code


class Gender(models.Model):
	code = models.CharField(max_length=20)
	class Meta:
		db_table = "Gender"
		verbose_name = "Gender"

	def __str__(self):
		return self.code

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
	first_name = models.CharField(max_length = 256,blank = True)
	last_name = models.CharField(max_length = 256,blank = True)
	gender = models.ForeignKey(Gender,on_delete=models.SET_NULL,blank=True,null=True)
	birthdate = models.DateField(blank=True,null=True)
	citizen_identity_card = models.DecimalField(max_digits=12,decimal_places=0,null=True,blank=True)
	email = models.EmailField(unique=True)
	phone_number = PhoneNumberField(region = "VI",unique=True)
	avatar = models.ImageField(default='avatars/avatar.png', upload_to='avatars/')
	location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
	status = models.ForeignKey(User_Status,on_delete=models.DO_NOTHING,blank=True,null=True)
	current_order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
	moderated = models.DateTimeField(blank=True, null=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "Profiles"
		verbose_name = "Profile"

	def __str__(self):
		return f"{self.user.username}"

	def birthdate_update(self,date):
		str_date = date.split("-")
		int_date = [int(i) for i in str_date]
		new_birthdate = datetime.date(*int_date)
		if new_birthdate > datetime.datetime.now().date():
			raise ValidationError("Ngày sinh không thể là ngày sau ngày hôm nay")
		self.birthdate = new_birthdate

	def update_profile(self,request):
		self.first_name = request.POST.get("first_name")
		self.last_name = request.POST.get("last_name")
		self.gender_id = request.POST.get("gender")

		validate_email(request.POST.get("email"))
		validate_international_phonenumber(request.POST.get("phone_number"))

		self.birthdate_update(request.POST.get("birthdate"))
		self.phone_number = request.POST.get("phone_number")
		self.email = request.POST.get("email")
		self.citizen_identity_card = request.POST.get("citizen_identity_card")

		self.save()

	def update_location(self,request):
		if self.location == None:
			self.location = Location.objects.create()

		self.location.lat = request.POST.get("lat")
		self.location.lng = request.POST.get("lng")
		self.location.address = request.POST.get("address")
		self.location.country = request.POST.get("country")
		self.location.region = request.POST.get("region")
		self.location.subregion_1 = request.POST.get("subregion_1")
		self.location.subregion_2 = request.POST.get("subregion_2")
		self.location.save()

	@property
	def is_customer(self):
		return Group.objects.get(name="Customers") in self.user.groups.all()

	@property
	def is_store_owner(self):
		return Group.objects.get(name="StoreOwners") in self.user.groups.all()

	@property
	def is_deliverer(self):
		return Group.objects.get(name="Deliverers") in self.user.groups.all()
