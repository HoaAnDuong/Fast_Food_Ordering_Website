import datetime

from django.core.exceptions import ValidationError,ObjectDoesNotExist
import json
from .models import *
from products.models import *

def ban_product(request,product):
    if not request.user.profile.is_moderator:
        raise ValidationError("Bạn không phải Người kiểm duyệt, không thể thực hiện hành động này")
    if request.POST.get("reason") == "" or request.POST.get("reason") == None:
        raise ValidationError("Không được để trống lý do thay đổi")
    if product.status.code != "active" and product.status.code != "disabled":
        raise ValidationError("Món ăn không thể bị chặn")

    reason = request.POST.get("reason")
    old_value = product.status.code
    product.status = Product_Status.objects.get(code = "banned")
    product.save()
    new_value = product.status.code
    description = f"{datetime.datetime.now()}: Người kiểm duyệt có tài khoản {request.user.username} đã chặn món {product.name} của cửa hàng {product.store.name}"

    changelog = Moderator_Changelog(moderator = request.user,action = Action.objects.get(code="ban"),
                                    target_id = product.id,target_type = "Product",
                                    old_value=old_value,new_value=new_value,
                                    description = description,reason = reason)
    changelog.save()
def unban_product(request,product):
    if not request.user.profile.is_moderator:
        raise ValidationError("Bạn không phải Người kiểm duyệt, không thể thực hiện hành động này")
    if request.POST.get("reason") == "" or request.POST.get("reason") == None:
        raise ValidationError("Không được để trống lý do thay đổi")
    if product.status.code != "banned":
        raise ValidationError("Món ăn không thể bị chặn")

    reason = request.POST.get("reason")
    old_value = product.status.code
    product.status = Product_Status.objects.get(code = "active")
    product.save()
    new_value = product.status.code
    description = f"{datetime.datetime.now()}: Người kiểm duyệt có tài khoản {request.user.username} đã bỏ chặn món {product.name} của cửa hàng {product.store.name}"

    changelog = Moderator_Changelog(moderator = request.user,action = Action.objects.get(code="unban"),
                                    target_id = product.id,target_type = "Product",
                                    old_value=old_value,new_value=new_value,
                                    description = description,reason = reason)
    changelog.save()
def verify_product(request,product):
    if not request.user.profile.is_moderator:
        raise ValidationError("Bạn không phải Người kiểm duyệt, không thể thực hiện hành động này")
    if request.POST.get("reason") == "" or request.POST.get("reason") == None:
        raise ValidationError("Không được để trống lý do thay đổi")
    if product.status.code != "pending":
        raise ValidationError("Món ăn không thể bị chặn")

    reason = request.POST.get("reason")
    old_value = product.status.code
    product.status = Product_Status.objects.get(code = "active")
    product.save()
    new_value = product.status.code
    description = f"{datetime.datetime.now()}: Người kiểm duyệt có tài khoản {request.user.username} đã xác nhận món {product.name} của cửa hàng {product.store.name}"

    changelog = Moderator_Changelog(moderator = request.user,action = Action.objects.get(code="unban"),
                                    target_id = product.id,target_type = "Product",
                                    old_value=old_value,new_value=new_value,
                                    description = description,reason = reason)
    changelog.save()
