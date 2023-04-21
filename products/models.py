from django.db import models
from djmoney.models.fields import MoneyField
from stores.models import Store
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError,ObjectDoesNotExist

# Create your models here.

class Category(models.Model):
    code = models.TextField(max_length=100,default = "")
    name = models.TextField(max_length=100,default = "")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Category"
        verbose_name = "Category"

    def __str__(self):
        return self.name

class Product_Status(models.Model):
    code = models.CharField(max_length=20)

    class Meta:
        db_table = "Product_Status"
        verbose_name = "Product_Status"

    def __str__(self):
        return self.code

class Product(models.Model):
    name = models.TextField(max_length=255)
    desciption = models.TextField(max_length=2048,blank = True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE,null=True,related_name="products")
    price = MoneyField(max_digits=256,decimal_places=2,default = 0,default_currency='VND')
    new_price = MoneyField(max_digits=256,decimal_places=2,default = 0,default_currency='VND')
    image = models.ImageField(default='products.png', upload_to='products/')
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING,blank=True,null=True)
    status = models.ForeignKey(Product_Status,on_delete=models.DO_NOTHING,blank=True,null=True)
    moderated = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255,null=True)

    class Meta:
        db_table = "Product"
        verbose_name = "Product"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

class Product_Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    review = models.TextField(blank=True)
    images = models.ImageField(upload_to='reviews/',null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Product_Review"
        verbose_name = "Product_Review"

class Product_Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="reports")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.TextField()
    images = models.ImageField(upload_to='reports/', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Product_Report"
        verbose_name = "Product_Report"


