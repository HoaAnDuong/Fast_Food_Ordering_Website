from django.db import models
from django.contrib.auth.models import User
from locations.models import Location
from products.models import Product
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from djmoney.models.fields import MoneyField
from foodapp.settings import MAX_ORDER_PRODUCTS_COUNT,MAX_DISTANCE,MAX_NUM_OF_STORES
from locations.utils import distance
from itertools import permutations
from djmoney.money import Money
from django.db import transaction
import sys

import datetime

# Create your models here.

class Delivery_Status(models.Model):
    code = models.CharField(max_length=20)

    class Meta:
        db_table = "Delivery_Status"
        verbose_name = "Delivery_Status"

    def __str__(self):
        return self.code


class Payment_Status(models.Model):
    code = models.CharField(max_length=20)

    class Meta:
        db_table = "Payment_Status"
        verbose_name = "Payment_Status"

    def __str__(self):
        return self.code

class Order_Status(models.Model):
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "Order_Status"
        verbose_name = "Order_Status"

class Payment_Method(models.Model):
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.code

class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer_orders')
    payment_method = models.ForeignKey(Payment_Method, on_delete=models.DO_NOTHING, blank=True, null=True)
    destination = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    total = MoneyField(max_digits=256,decimal_places=2,default_currency='VND',default=0)
    product_total = MoneyField(max_digits=256,decimal_places=2,default_currency='VND',default=0)
    delivery_fee = MoneyField(max_digits=256,decimal_places=2,default_currency='VND',default=0)
    nighttime_fee = MoneyField(max_digits=256,decimal_places=2,default_currency='VND',default=0)
    delivery_status = models.ForeignKey(Delivery_Status,on_delete=models.DO_NOTHING,blank=True,null=True)
    payment_status = models.ForeignKey(Payment_Status,on_delete=models.DO_NOTHING,blank=True,null=True)
    order_status = models.ForeignKey(Order_Status,on_delete=models.DO_NOTHING,blank=True,null=True)
    image = models.ImageField(default="orders/order.png",upload_to="orders")
    moderated = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Order"
        verbose_name = "Order"

    def __str__(self):
        return f"{self.customer.username} - {self.created}"

    @property
    def total_quantity(self):
        quantity = 0

        for order_product in self.order_products.all():
            quantity += order_product.quantity
        return quantity

    @property
    def store_list(self):
        order_products = self.order_products.all()
        store_list = []
        for i in order_products:
            if i.status.code != "cancelled" and not i.product.store in store_list:
                store_list.append(i.product.store)
        return store_list

    @property
    def customer_store(self):
        try:
            with transaction.atomic():
                return self.customer.store
        except:
            return None
    @property
    def deliverer(self):
        try:
            with transaction.atomic():
                return self.delivery.deliverer
        except:
            return None
    def expire_check(self):
        created_date = self.created
        if created_date.date() < datetime.datetime.now().date():
            if self.order_status.code == "pending":
                expired_status = Order_Status.objects.get(code="expired")
                self.order_status = expired_status
                self.save()
                return True
        else:
            return False
    def calculate_total(self):
        self.total = 0
        self.product_total = 0
        self.delivery_fee = 0
        self.nighttime_fee = 0
        for i in self.order_products.all():
            if i.status.code != "cancelled":
                self.product_total += i.total
        self.total += self.product_total

        total_length = self.shortest_path()["total_length"] if not hasattr(self,'delivery') or self.delivery.total_length == 0 else self.delivery.total_length
        self.delivery_fee += Money(12000,'VND')
        if total_length > 2:
            self.delivery_fee += (total_length-2) * Money(4000,'VND')
        self.total += self.delivery_fee

        now_hour = datetime.datetime.now().time()

        if now_hour >= datetime.time(19,0,0) or now_hour <= datetime.time(6,0,0):
            self.nighttime_fee = Money(8000,'VND')
        self.total += self.nighttime_fee

        self.save()
        return self.total

    def shortest_path(self,with_start_pos=True):
        if hasattr(self,'delivery') and with_start_pos:
            start_pos = self.delivery.start_point
        else:
            start_pos = None

        stores = self.store_list
        end_pos = self.destination

        min_total_length = sys.maxsize
        min_path = []
        for stores_list in permutations(stores):
            total_length = 0
            path = []
            if start_pos != None:
                path.append(start_pos)
            path+=[item.location for item in stores_list]
            path.append(end_pos)
            for i in range(1 if start_pos else 0,len(path)-1):
                total_length+=distance(path[i],path[i+1])

            if total_length < min_total_length:
                min_total_length = total_length
                min_path = path
        return {"total_length":min_total_length,"path":min_path}


    def add_product(self,product,quantity,note):
        store_list = self.store_list
        if self.order_status.code != "pending":
            raise ValidationError("Bạn không thể thực hiện thay đổi trên đơn hàng này.")
        if product.store not in store_list:
            if len(store_list) >= MAX_NUM_OF_STORES:
                raise ValidationError(f"Bạn không thể đặt thêm món từ 1 cửa hàng mới.Số lượng cửa hàng đã vượt quá {MAX_NUM_OF_STORES}.")
        if self.order_status.code != "pending":
            raise ValidationError("Bạn không thể thực hiện thay đổi trên đơn hàng này.")
        if product.store == self.customer_store:
            raise ValidationError("Bạn không thể đặt đơn hàng từ shop của chính bạn")
        quantity = int(quantity)
        if product.store.status.code != "active":
            raise ValidationError("Bạn không thể đặt hàng từ cửa hàng này")
        if product.status.code != "active":
            raise ValidationError("Món ăn không sẵn sàng để được đặt")

        if quantity < 0: raise ValueError("Số lượng không thể nhỏ hơn 0")

        if self.total_quantity + quantity <= MAX_ORDER_PRODUCTS_COUNT:
            self.order_products.create(order = self,product=product,price = product.price,quantity=quantity,
                                    total = product.price*quantity,note=note,status = Order_Product_Status.objects.get(code = "pending"))
            self.calculate_total()
            self.logs.create(log = f"{datetime.datetime.now()}: Đã thêm sản phẩm {product.name} với số lượng {quantity}")
        else:
            raise ValueError(f"Tổng số lượng hàng được đặt không thể vượt quá {MAX_ORDER_PRODUCTS_COUNT}")

    def update_product(self,product,quantity,note):
        if self.order_status.code != "pending":
            raise ValidationError("Bạn không thể thực hiện thay đổi trên đơn hàng này.")
        if product.store == self.customer_store:
            raise ValidationError(f"Bạn không thể đặt món từ cửa hàng của chính mình")
        if product.store.status.code != "active":
            raise ValidationError("Bạn không thể đặt hàng từ cửa hàng này")
        if product.status.code != "active":
            raise ValidationError("Món ăn không sẵn sàng để được đặt")

        quantity = int(quantity)
        if quantity < 0: raise ValueError("Số lượng không thể nhỏ hơn 0")
        order_product = self.order_products.get(product=product)
        if self.total_quantity - order_product.quantity + quantity <= MAX_ORDER_PRODUCTS_COUNT:
            order_product.price = product.price
            order_product.quantity = quantity
            order_product.note = note
            order_product.total = product.price * quantity
            order_product.save()
            self.logs.create(log=f"{datetime.datetime.now()}: Đã cập nhật sản phẩm {product.name}, thay đổi số lượng thành {quantity}")
            self.calculate_total()
        else:
            raise ValueError(f"Tổng số lượng hàng được đặt không thể vượt quá {MAX_ORDER_PRODUCTS_COUNT}")

    def delete_product(self, product):
        if self.order_status.code != "pending": raise ValidationError(
            "Bạn không thể thực hiện thay đổi trên đơn hàng này."
        )
        order_product = self.order_products.get(product=product)

        quantity = order_product.quantity

        order_product.delete()
        self.logs.create(
            log=f"{datetime.datetime.now()}: Đã xóa sản phẩm {product.name} với số lượng {quantity} ra khỏi giỏ hàng")


        self.calculate_total()

    def cancel_product(self, request):
        order_product = self.order_products.get(product__id=request.POST.get("product_id"))
        if order_product.status != "submitted":
            raise ValidationError(f"Món ăn {order_product.product.name} không thể bị hủy")
        order_product.status = Order_Product_Status.get(code="cancelled")

    def update_location(self,request):
        if self.order_status.code != "pending": raise ValidationError(
            "Bạn không thể thực hiện thay đổi trên đơn hàng này."
        )
        self.destination.lat = float(request.POST.get("lat"))
        self.destination.lng = float(request.POST.get("lng"))
        self.destination.address = request.POST.get("address")
        self.destination.country = request.POST.get("country")
        self.destination.region = request.POST.get("region")
        self.destination.subregion_1 = request.POST.get("subregion_1")
        self.destination.subregion_2 = request.POST.get("subregion_2")

        self.delivery.total_length = float(request.POST.get('total_length'))
        self.delivery.save()

        self.logs.create(
            log=f"{datetime.datetime.now()}: Đã thay đổi vị trí giao hàng thành {self.destination.address}. Tổng quảng đường giao hàng bây giờ là {self.delivery.total_length}")
        self.destination.save()


    def validate(self):
        if self.total_quantity == 0:
            raise ValidationError(f"Đơn hàng hiện tại chưa có món ăn nào")
        if len(self.store_list) > MAX_NUM_OF_STORES:
            raise ValidationError(f"Số cửa hàng được đặt tối đa là {MAX_NUM_OF_STORES}. Bạn đã đặt hàng trên {len(self.store_list)} cửa hàng")

        for store in self.store_list:
            if store == self.customer_store:
                raise ValidationError(f"Bạn không thể đặt món từ cửa hàng của chính mình")
            if store.status.code != "active":
                raise ValidationError(f"Không thể đặt hàng từ Cửa hàng {store.name} - {store.location.address}")
            if distance(store.location, self.destination) > MAX_DISTANCE:
                raise ValidationError(f"Khoảng cách từ vị trí đặt hàng đến cửa hàng {store.name} - {store.location.address} vượt quá {MAX_DISTANCE} km.")
            if not store.is_open:
                raise ValidationError(f"Cửa hàng {store.name} - {store.location.address} hiện tại không mở cửa")

        if self.total_quantity > MAX_ORDER_PRODUCTS_COUNT:
            raise ValidationError(f"Số lượng sản phẩm được đặt không quá {MAX_ORDER_PRODUCTS_COUNT}")

        for order_product in self.order_products.all():
            if order_product.product.status.code != "active":
                raise ValidationError(f"Sản phẩm {order_product.product.name} không có sẵn để đặt")

    def submit_order(self):
        if self.order_status.code != "pending": raise ValidationError(
            "Bạn không thể thực hiện thay đổi trên đơn hàng này."
        )
        if not self.expire_check():
            self.validate()

            self.delivery.find_deliverer()

            for item in self.order_products.all():
                item.status = Order_Product_Status.objects.get(code="submitted")
                item.save()

            self.delivery_status = Delivery_Status.objects.get(code="delivering")
            self.calculate_total()
            self.order_status = Order_Status.objects.get(code = "submitted")
            self.logs.create(
                log=f"{datetime.datetime.now()}: Đơn hàng đã được xác nhận")
            self.save()

    def cancel_order(self):
        pass

class Order_Product_Status(models.Model):
    code = models.CharField(max_length=20)

    class Meta:
        db_table = "Order_Product_Status"
        verbose_name = "Order_Product_Status"

    def __str__(self):
        return self.code

class Order_Product(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_products")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="order_products")
    quantity = models.PositiveIntegerField()
    image = models.ImageField(default='order_products/order_product.png', upload_to='order_products/')
    price = MoneyField(max_digits=256, decimal_places=2, default_currency='VND', default=0)
    total = MoneyField(max_digits=256, decimal_places=2, default_currency='VND', default=0)
    note = models.TextField(max_length=255,blank=True,null=True)
    status = models.ForeignKey(Order_Product_Status,on_delete=models.DO_NOTHING,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Order_Product"
        verbose_name = "Order_Product"
        unique_together = ["order","product"]
    def __str__(self):
        return f"{self.product.name} {self.order.__str__()}"

class Order_Log(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="logs")
    log = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Order_Log"
        verbose_name = "Order_Log"


class Order_Review(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name="review")
    rating = models.FloatField(default=0)
    review = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Order_Review"
        verbose_name = "Order_Review"