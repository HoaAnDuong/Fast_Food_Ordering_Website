from django.db import models
from django.contrib.auth.models import User
from locations.utils import distance
from orders.models import Order,Order_Product_Status,Order_Status,Payment_Status
from orders.models import Delivery_Status as Order_Delivery_Status
import datetime
from django.db.models import Count, F, Value, Q
from foodapp.settings import MAX_CHOOSE_DELIVERY_DISTANCE,MAX_GET_PRODUCT_DISTANCE
from django.core.exceptions import ValidationError
from locations.models import Location
from django.db import transaction
from foodapp.utils import image_upload
from django.contrib.auth import authenticate

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
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Deliverer_Profile"
        verbose_name = "Deliverer_Profile"

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
    def update_profile(self,request):
        self.driver_license = request.POST.get('driver_license')
        self.save()
    def check_in(self,request):
        start_time = datetime.datetime.now()

        end_hrs_min = [int(i) for i in request.POST.get('end_time').split(":")]
        end_time = datetime.datetime.now().replace(hour=end_hrs_min[0], minute=end_hrs_min[1],second=0,microsecond=0)

        if start_time >= end_time:
            raise ValueError("Start time must be smaller than end time")
        else:
            self.start_time = start_time
            self.end_time = end_time
            self.save()
    def update_end_time(self,request):
        end_hrs_min = [int(i) for i in request.POST.get('end_time').split(":")]
        end_time = datetime.datetime.now().replace(hour=end_hrs_min[0], minute=end_hrs_min[1], second=0, microsecond=0)
        if self.start_time == None or self.start_time.date() != datetime.datetime.now().date():
            self.start_time = datetime.datetime.now()
        if self.start_time >= end_time:
            raise ValueError("Start time must be smaller than end time")
        else:
            self.end_time = end_time
            self.save()
    @property
    def is_active(self):
        return self.status.code == "active" and datetime.datetime.now() < self.end_time

    @property
    def name(self):
        return f"{self.user.profile.last_name} {self.user.profile.first_name}"
    @property
    def email(self):
        return self.user.profile.email
    @property
    def phone_number(self):
        return self.user.profile.phone_number
    @property
    def current_delivery(self):
        try:
            with transaction.atomic():
                return self.deliveries.filter(Q(status__code = "delivering")|Q(status__code = "arrived"))[0]
        except:
            return None

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")
    deliverer = models.ForeignKey(Deliverer_Profile, on_delete=models.CASCADE, related_name='deliveries',
                                  blank=True, null=True)
    start_point = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    total_length = models.FloatField(default=0)
    status = models.ForeignKey(Delivery_Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    arrived = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = "Deliverery"
        verbose_name = "Deliverery"

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
                                                .filter(current_location__region = self.order.destination.region,status__code = "active")\
                                                .exclude(user = self.order.customer)\
                                                .annotate(distance = ((F("current_location__lat")-point.lat) ** 2.
                                                    + (F("current_location__lng")-point.lng) ** 2.)
                                                    ** 0.5 * 111.319)\
                                                .filter(distance__lte = MAX_CHOOSE_DELIVERY_DISTANCE)\
                                                .order_by('distance')

            if len(deliverers) != 0:
                for chosen_deliverer in deliverers:

                    if chosen_deliverer.is_active and chosen_deliverer.current_delivery == None:
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
    def get_product(self,request):
        order_product = self.order.order_products.get(product__id = request.POST.get("product_id"))
        if order_product.status.code != "submitted":
            raise ValidationError(f"Bạn không cần giao món {order_product.name} nữa.")

        if request.FILES.get('image') == None: raise FileNotFoundError("Ảnh chưa được tải lên")

        store = order_product.product.store
        if distance(store.location,self.deliverer.current_location) > MAX_GET_PRODUCT_DISTANCE:
            raise ValidationError(f"Khoảng cách nhận hàng vượt quá {MAX_GET_PRODUCT_DISTANCE} km (Thực tế: {distance(store.location,self.deliverer.current_location)}). Người giao hàng vui lòng đến gần cửa hàng hơn để nhận hàng.")

        image_upload(subfolders="order_products", instance=order_product, file=request.FILES['image'])
        order_product.status = Order_Product_Status.objects.get(code = "delivering")
        self.order.logs.create(log = f"{datetime.datetime.now()}: Người giao hàng đã nhận món {order_product.product.name} với số lượng {order_product.quantity}")
        order_product.save()

    def update_product_image(self,request):
        order_product = self.order.order_products.get(product__id=request.POST.get("product_id"))
        if order_product.status.code != "delivering":
            raise ValidationError(f"Bạn không thể sửa ảnh minh chứng của món {order_product.name} bây giờ.")
        if request.FILES.get('image') == None: raise FileNotFoundError("Ảnh chưa được tải lên")
        image_upload(subfolders="order_products", instance=order_product, file=request.FILES['image'])



    def get_store_products(self,request):
        if request.FILES.get('image') == None: raise FileNotFoundError("Ảnh chưa được tải lên")
        order_products = self.order.order_products.filter(product__store__id=request.POST.get("store_id"))

        for order_product in order_products:
            if distance(order_product.product.store.location, self.deliverer.current_location) > MAX_GET_PRODUCT_DISTANCE:
                raise ValidationError(
                    f"Khoảng cách nhận hàng vượt quá {MAX_GET_PRODUCT_DISTANCE} km (Thực tế: {distance(order_product.product.store.location, self.deliverer.current_location)}). Người giao hàng vui lòng đến gần cửa hàng hơn để nhận hàng.")

            if order_product.status.code == "submitted":
                image_upload(subfolders="order_products", instance=order_product, file=request.FILES['image'])
                order_product.status = Order_Product_Status.objects.get(code="delivering")
                self.order.logs.create(
                    log=f"{datetime.datetime.now()}: Người giao hàng đã nhận món {order_product.product.name} với số lượng {order_product.quantity}")
                order_product.save()

    def arrived_check(self):

        if self.status.code == "arrived": return True
        if distance(self.deliverer.current_location,self.order.destination) > MAX_GET_PRODUCT_DISTANCE:
            return False
        for item in self.order.order_products.all():
            if item.status.code != "delivering" and item.status.code != "cancelled":
                return False
        self.status = Delivery_Status.objects.get(code = "arrived")
        self.arrived = datetime.datetime.now()

        self.order.order_status = Order_Status.objects.get(code = "arrived")
        self.order.delivery_status = Order_Delivery_Status.objects.get(code = "arrived")
        self.order.logs.create(log = f"{datetime.datetime.now()}: Người giao hàng đã đến điểm giao hàng. Khách hàng vui lòng đến nhận hàng.")
        self.order.save()
        self.save()
        return True
    def dispatch(self,request):
        if request.FILES.get('image') == None: raise FileNotFoundError("Ảnh chưa được tải lên")
        if distance(self.deliverer.current_location,self.order.destination) > MAX_GET_PRODUCT_DISTANCE:
            raise ValidationError(f"Khoảng cách nhận hàng vượt quá {MAX_GET_PRODUCT_DISTANCE} km (Thực tế: {distance(self.deliverer.current_location,self.order.destination)}). Người giao hàng vui lòng đến gần vị trí giao hàng hơn.")
        for item in self.order.order_products.all():
            if item.status.code != "cancelled" and item.status.code != "delivering":
                raise ValidationError(f"Món ăn {item.product.name} vẫn chưa được lấy và vận chuyển")

        if self.status.code != "arrived":
            raise ValidationError("Bạn không thể giao hàng cho khách hàng bây giờ")

        for item in self.order.order_products.all():
            item.status = Order_Product_Status.objects.get(code = "received")


        order = self.order
        image_upload(subfolders="orders", instance=order, file=request.FILES['image'])
        order.payment_status = Payment_Status.objects.get(code = "paid")
        order.delivery_status = Order_Delivery_Status.objects.get(code = "completed")
        order.order_status = Order_Status.objects.get(code = "completed")
        order.logs.create(
            log=f"{datetime.datetime.now()}: Đơn hàng đã được giao thành công!")
        self.order.save()

        self.status = Delivery_Status.objects.get(code="completed")
        self.save()

    def ghosted_report(self,request):

        if self.status.code != "arrived":
            raise ValidationError("Bạn không thể báo cáo việc khách hàng không nhận hàng và thanh toán ngay bây giờ.")

        if datetime.datetime.now() - self.arrived > datetime.timedelta(minutes=15):
            if request.FILES.get('image') == None: raise FileNotFoundError("Ảnh chưa được tải lên")
            if distance(self.deliverer.current_location, self.order.destination) > MAX_GET_PRODUCT_DISTANCE:
                raise ValidationError(
                    f"Khoảng cách nhận hàng vượt quá {MAX_GET_PRODUCT_DISTANCE} km (Thực tế: {distance(self.deliverer.current_location, self.order.destination)}). Người giao hàng vui lòng đến gần vị trí giao hàng hơn.")

            if not authenticate(request, username=request.user.username, password=request.POST.get("password")):
                raise ValidationError("Bạn đã nhập sai mật khẩu")

            for item in self.order.order_products.all():
                if item.status.code != "cancelled" and item.status.code != "delivering":
                    raise ValidationError(f"Món ăn {item.product.name} vẫn chưa được lấy và vận chuyển")
            for item in self.order.order_products.all():
                item.status = Order_Product_Status.objects.get(code="ghosted")

            order = self.order
            image_upload(subfolders="orders", instance=order, file=request.FILES['image'])
            order.delivery_status = Order_Delivery_Status.objects.get(code="incompleted")
            order.order_status = Order_Status.objects.get(code="ghosted")
            order.logs.create(
                log=f"{datetime.datetime.now()}: Bạn đã không nhận và thanh toán đơn hàng! Hành vi này sẽ được lưu vào hệ thống và sẽ có biện pháp xử lý cụ thể.")
            self.order.save()

            self.status = Delivery_Status.objects.get(code="incompleted")
            self.save()
        else:
            raise ValidationError("Bạn cần phải đợi 15 phút kể từ khi có mặt tại điểm giao hàng để báo cáo việc khách hàng không nhận hàng và thanh toán ngay bây giờ.")


class Delivery_Point(models.Model):
    priority = models.PositiveIntegerField(default=1)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="points", null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ["priority", "location"]