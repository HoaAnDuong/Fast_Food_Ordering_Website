from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(Order_Product)
admin.site.register(Order_Product_Status)
admin.site.register(Order_Log)
admin.site.register(Order_Review)
admin.site.register(Order_Status)
admin.site.register(Payment_Status)
admin.site.register(Payment_Method)
admin.site.register(Delivery_Status)