from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from stores.models import Store
from orders.models import Order

# Create your models here.

class Complaint_Status(models.Model):
    code = models.CharField(max_length=20)

class Complaint(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    content = models.TextField(max_length=1024,default = "")
    image = models.ImageField(upload_to='complaints/', null=True)
    status = models.ForeignKey(Complaint_Status,on_delete=models.DO_NOTHING)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

class Product_Complaint(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Store_Complaint(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

class Order_Complaint(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    order = models.ForeignKey(Store, on_delete=models.CASCADE)
