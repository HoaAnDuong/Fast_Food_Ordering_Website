from django.shortcuts import render
from .utils import *
from .models import *
from django.db import transaction
from django.contrib import messages
from delivery.models import Delivery,Delivery_Status
from django.contrib.auth import authenticate
from django.http import HttpResponse,Http404
import json
# Create your views here.

def CurrentOrderView(request):
    ctx = {}
    if not request.user.is_anonymous:
        current_order_expire_check(request.user)
        current_order = request.user.profile.current_order
        ctx["remain_cancellations"] = request.user.profile.remain_cancellations
        ctx["current_order"] = current_order
        if current_order:
            ctx["store_list"] = current_order.store_list
            # ctx["shortest_path"] = current_order.shortest_path()

        ctx["payment_methods"] = Payment_Method.objects.all()

        if request.method == "POST":
            match request.POST.get("form_tag"):
                case "create_order":
                    print("Đang tạo đơn hàng mới")
                    current_order = create_new_order(request.user)
                    if not hasattr(current_order,'delivery'):
                        Delivery.objects.create(order = current_order,status = Delivery_Status.objects.get(code="pending"))

                case "update_order":
                    if not hasattr(current_order,'delivery'):
                        Delivery.objects.create(order = current_order,status = Delivery_Status.objects.get(code="pending"))
                    current_order.payment_method = Payment_Method.objects.get(id = request.POST.get("payment_method"))
                    current_order.calculate_total()
                    current_order.save()
                case "location":
                    if not hasattr(current_order,'delivery'):
                        Delivery.objects.create(order = current_order,status = Delivery_Status.objects.get(code="pending"))
                    current_order.update_location(request)
                    current_order.destination.save()

                    current_order.calculate_total()

                case "update_product":
                    product = Product.objects.get(id=request.POST.get("product_id"))
                    current_order.update_product(product,quantity=request.POST.get("quantity"),note=request.POST.get("note"))

                case "delete_product":
                    product = Product.objects.get(id=request.POST.get("product_id"))
                    current_order.delete_product(product)
                case "cancel_product":
                    if not authenticate(request,username = request.user.username,password=request.POST.get("password")):
                        raise ValidationError("Bạn đã nhập sai mật khẩu")
                    product = Product.objects.get(id=request.POST.get("product_id"))
                    current_order.cancel_product(product)
                case "submit_order":
                    if not authenticate(request,username = request.user.username,password=request.POST.get("password")):
                        raise ValidationError("Bạn đã nhập sai mật khẩu")
                    if not hasattr(current_order,'delivery'):
                        Delivery.objects.create(order = current_order,status = Delivery_Status.objects.get(code="pending"))
                    with transaction.atomic():
                        try:
                            current_order.update_location(request)
                            current_order.destination.save()
                            current_order.submit_order()
                        except Exception as e:
                            current_order.logs.create(log = f"{datetime.datetime.now()}: {e}")
                case "cancel_order":
                    if not authenticate(request, username=request.user.username, password=request.POST.get("password")):
                        raise ValidationError("Bạn đã nhập sai mật khẩu")
                    with transaction.atomic():
                        try:
                            pass
                        except Exception as e:
                            current_order.logs.create(log=f"{datetime.datetime.now()}: {e}")
                    current_order.cancel_order()
                case "cancel_others":
                    current_order.cancel_others()
                case "review_product":
                    product = Product.objects.get(id=request.POST.get("product_id"))
                    product.make_review(request)


            current_order = request.user.profile.current_order
            ctx["current_order"] = current_order
        if current_order and current_order.order_status.code != "pending" and current_order.order_status.code != "expired":
            route = current_order.delivery.points.all().order_by('priority')

            ctx["route"] = {}
            ctx["route"]["start"] = route[0]
            ctx["route"]["destination"] = route[len(route)-1]
            ctx["route"]["stores"] = route[1:len(route)-1]
    else:
        ctx["current_order"] = None

    return render(request, 'Site/CurrentOrder.html', ctx)

def GetCurrentOrderData(request):
    ctx = {}
    if request.method == 'GET':
        if not request.user.is_anonymous:
            current_order = request.user.profile.current_order
            if current_order:

                current_order.calculate_total()
                ctx = {
                    "order_status":current_order.order_status.code,
                    "delivery_status":current_order.delivery_status.code,
                    "payment_status":current_order.payment_status.code,
                    "product_total":current_order.product_total.__str__(),
                    "delivery_fee":current_order.delivery_fee.__str__(),
                    "nighttime_fee":current_order.nighttime_fee.__str__(),
                    "total":current_order.total.__str__(),
                    "store_list":[
                        {
                            "name":item.name,
                            "address":item.location.address,
                            "lat":item.location.lat,
                            "lng":item.location.lng
                        }
                        for item in current_order.store_list
                    ],
                    "order_product":[
                        {
                            "slug":item.product.slug,
                            "name":item.product.name,
                            "image_url":item.product.image.url,
                            "price":item.price.__str__(),
                            "quantity":item.quantity,
                            "total":item.total.__str__(),
                            "status":item.status.code,
                            "updated":item.updated.__str__(),
                            "note":item.note
                        }
                        for item in current_order.order_products.all()
                    ],
                    "logs":[
                        {
                            "created":item.created.__str__(),
                            "log":item.log
                        }
                        for item in current_order.logs.all()
                    ]
                }
                return HttpResponse(json.dumps(ctx,indent=4),status=200)

            return HttpResponse(status=400)
    else:
        return Http404()


def DelivererCurrentLocation(request):
    ctx = {}
    if request.method == 'GET':
        if not request.user.is_anonymous:
            current_order = request.user.profile.current_order
            if current_order:
                deliverer = current_order.delivery.deliverer
                ctx = {
                    "is_active": deliverer.is_active,
                    "deliverer_lat": deliverer.current_location.lat,
                    "deliverer_lng": deliverer.current_location.lng
                }
                return HttpResponse(json.dumps(ctx),status = 200)
            return HttpResponse(status = 400)
    else:
        return Http404()
