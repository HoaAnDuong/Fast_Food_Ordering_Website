from django.db import models
from djmoney.models.fields import MoneyField
from stores.models import Store
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from foodapp.utils import image_upload
from django.db.models import Q,Avg,Count,Sum

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
    description = models.TextField(max_length=2048,blank = True)
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

    @property
    def average_rating(self):
        average_rating = self.reviews.aggregate(Avg("rating"),Count('author'))
        return average_rating

    @property
    def total_revenue(self):
        order_products = self.order_products.exclude(Q(status__code = "pending")|Q(status__code = "cancelled")|Q(status__code = "ghosted"))
        return order_products.aggregate(Sum("total"))["total__sum"]
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

    def make_review(self,request):
        user = request.user
        if not request.user.profile.purchased_product(self):
            raise ValidationError(f"Bạn chưa đặt món {self.name}, nên chưa thể viết bài đánh giá.")
        rating = float(request.POST.get('rating'))
        title = request.POST.get('title')
        review_content = request.POST.get('review')
        image = request.FILES.get('image')
        print(image)
        if rating < 0 or rating > 5:
            raise ValueError("Giá trị của lượt đánh giá phải nằm giữa 0 và 5")
        try:
            with transaction.atomic():
                review = Product_Review.objects.get(product=self,author=user)
                review.rating = rating
                review.title = title
                review.review = review_content

        except:
            review = Product_Review.objects.create(product=self,author=user,
                                                   rating=rating,title=title,review=review_content)
        if image != None:
            image_upload('reviews', review, image)
        review.save()
    def delete_product(self):
        if self.status.code != "pending":
            raise ValidationError("Không thể xóa món này")
        self.delete()
    def disable_product(self):
        if self.status.code != "active":
            raise ValidationError("Không thể khóa món này")
        self.status = Product_Status.objects.get(code = "disabled")
        self.save()

    def active_product(self):
        if self.status.code != "disabled":
            raise ValidationError("Không thể mở khóa món này")
        self.status = Product_Status.objects.get(code = "active")
        self.save()

    def update_product(self,request):
        print(request)
        self.name = request.POST.get("name")
        self.price.amount = float(request.POST.get("price"))
        self.description = request.POST.get("description")
        self.category = Category.objects.get(id = request.POST.get('category_id'))
        self.save()
    def image_upload(self,request):
        image = request.FILES.get("image")
        if image != None:
            image_upload('products', self, image)


class Product_Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    title = models.TextField(blank=True,max_length=128)
    review = models.TextField(blank=True,max_length=2048)
    image = models.ImageField(upload_to='reviews/',null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Product_Review"
        verbose_name = "Product_Review"
        unique_together = ["product","author"]

    @property
    def is_updated(self):
        return self.created != self.updated

class Product_Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="reports")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(blank=True, max_length=128)
    report = models.TextField(max_length=2048)
    images = models.ImageField(upload_to='reports/', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Product_Report"
        verbose_name = "Product_Report"


