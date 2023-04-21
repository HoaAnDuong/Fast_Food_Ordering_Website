from django.db import models
from locations.models import  Location
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from locations.utils import distance

WEEKDAYS = [
  (0, "Monday"),
  (1, "Tuesday"),
  (2, "Wednesday"),
  (3, "Thursday"),
  (4, "Friday"),
  (5, "Saturday"),
  (6, "Sunday"),
]

# Create your models here.

class Store_Status(models.Model):
	code = models.CharField(max_length=20)

	class Meta:
		db_table = "Store_Status"
		verbose_name = "Store_Status"

	def __str__(self):
		return self.code


class Store(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="store")
	name = models.CharField(max_length = 256,blank = False)
	business_code = models.CharField(max_length =10,blank=True,null=True)
	tax_identification = models.CharField(max_length =13,blank=True,null=True)
	location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
	description = models.TextField(max_length = 512,blank=True)
	avatar = models.ImageField(default='stores/store.png', upload_to='stores/')
	status = models.ForeignKey(Store_Status,on_delete=models.SET_NULL,blank=True,null=True)
	slug = models.SlugField(max_length=255,null=True)
	moderated = models.DateTimeField(blank=True,null=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "Store"
		verbose_name = "Store"

	def __str__(self):
		return f"{self.name} - {self.user.profile.first_name} {self.user.profile.last_name}"

	@property
	def is_open(self):
		today = datetime.datetime.now()
		try:
			now_weekday = today.weekday()
			now_hour = today.time()
			today_opening_hour =  self.opening_hours.get(weekday=now_weekday)
			return self.status == "active" and now_hour >= today_opening_hour.from_hour and now_hour <= today_opening_hour.to_hour
		except:
			return False
	def distance_to(self,location):
		return distance(self.location,location)

	def update_store(self,request):
		self.name = request.POST.get("name")
		self.business_code = request.POST.get("business_code")
		self.tax_identification = request.POST.get("tax_identification")
		self.description = request.POST.get("description")

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

class Store_Opening_Hours(models.Model):
	store = models.ForeignKey(Store,on_delete=models.CASCADE,related_name="opening_hours")
	weekday = models.IntegerField(choices=WEEKDAYS,blank=True,null=True)
	from_hour = models.TimeField(blank=True,null=True)
	to_hour = models.TimeField(blank=True,null=True)
	class Meta:
		unique_together = ['store','weekday']

	def __str__(self):
		return f"{self.store.name} {self.get_weekday_display()} {self.from_hour} {self.to_hour}"

	def update(self,str_from_hour,str_to_hour):
		if str_from_hour == "" and str_to_hour == "":
			self.from_hour = None
			self.to_hour = None
		else:
			try:
				from_hour = datetime.datetime.strptime(str_from_hour,"%H:%M").time()
				to_hour = datetime.datetime.strptime(str_to_hour,"%H:%M").time()
				assert from_hour < to_hour
				self.from_hour = from_hour
				self.to_hour = to_hour
				self.save()
			except Exception as e:
				raise ValidationError(f"Thời gian nhập của {self.get_weekday_display()} vào không hợp lệ")


class Store_Image(models.Model):
	store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="images")
	image = models.ImageField(default='stores/images/store_image.png', upload_to='stores/images')