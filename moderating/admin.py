from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Complaint)
admin.site.register(Complaint_Status)
admin.site.register(Store_Complaint)
admin.site.register(Product_Complaint)
admin.site.register(Order_Complaint)
