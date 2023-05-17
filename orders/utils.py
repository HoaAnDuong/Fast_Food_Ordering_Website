from locations.models import Location
from .models import *
import datetime
from django.core.exceptions import ValidationError,ObjectDoesNotExist

def order_expire_check(order):
    if order != None:
        return order.expire_check()
    return False
def current_order_expire_check(user):
    current_order = user.profile.current_order
    if order_expire_check(current_order) == True:
        user.profile.current_order = None
        user.profile.save()

def create_new_order(user):
    if user.profile.current_order == None or user.profile.current_order.order_status.code == "cancelled" or user.profile.current_order.order_status.code  == "completed":
        user.profile.current_order = create_order(user)
        user.profile.save()
    return user.profile.current_order

def create_order(user):

    if user.profile.is_customer:
        user_location = user.profile.location
        new_location = Location.objects.create(address=user_location.address,country=user_location.country,
                                               region=user_location.region,subregion_1=user_location.subregion_1,subregion_2=user_location.subregion_2,
                                                lat = user_location.lat,lng = user_location.lng)
        unpaid_status = Payment_Status.objects.get(code="unpaid")
        delivery_pending_status = Delivery_Status.objects.get(code="pending")
        order_pending_status = Order_Status.objects.get(code = "pending")

        order = Order.objects.create(customer=user,destination=new_location,
                                     payment_status=unpaid_status,delivery_status = delivery_pending_status,
                                     order_status = order_pending_status)
        order.logs.create(log = f"{order.created.__str__()}: Đơn hàng đã được khởi tạo")
        user.profile.current_order = order
        user.profile.save()
        print(user.profile.current_order)
        return order
    else:
        raise ValidationError("Bạn không phải là Khách Hàng, bạn không thể tạo ra một đơn hàng mới.")

