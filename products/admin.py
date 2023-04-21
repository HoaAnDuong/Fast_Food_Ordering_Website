from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(Product_Review)
admin.site.register(Product_Report)
admin.site.register(Product_Status)
admin.site.register(Category)