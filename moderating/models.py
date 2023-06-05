from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from stores.models import Store
from orders.models import Order

# Create your models here.

class Complaint_Status(models.Model):
    code = models.CharField(max_length=20)
    def __str__(self):
        return self.code


class Complaint(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    content = models.TextField(max_length=1024,default = "")
    image = models.ImageField(upload_to='complaints/', null=True)
    status = models.ForeignKey(Complaint_Status,on_delete=models.DO_NOTHING)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    target_id = models.BigIntegerField(blank=True,null=True)
    targer_type = models.CharField(max_length=255,default = "")
    def create_complaint(self,request,instance):
        pass
class Action(models.Model):
    code = models.CharField(max_length=20)
    def __str__(self):
        return self.code
class Moderator_Changelog(models.Model):
    moderator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='changelogs')
    action = models.ForeignKey(Action, on_delete=models.DO_NOTHING)
    target_id = models.BigIntegerField(blank=True, null=True)
    target_type = models.CharField(max_length=255, default="")
    old_value = models.TextField(default = "")
    new_value = models.TextField(default = "")
    description = models.TextField(default = "",max_length=1024)
    reason = models.TextField(default = "",max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.moderator} {self.action} {self.target_type} {self.target_id}"

    def create_changlog(self,request,instance):
        pass




