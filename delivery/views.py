from django.shortcuts import render
from profiles.models import *
from profiles.forms import ProfileAvatarForm
from .utils import *
from django.http import HttpResponse,Http404
import json
from foodapp.utils import avatar_change
from django.contrib import messages
from django.db import transaction
from orders.models import Payment_Method
# Create your views here.

def DelivererProfileView(request):
    ctx = {}

    profile = Profile.objects.get(user=request.user)

    avatar_form = ProfileAvatarForm(instance=profile)
    ctx["avatar_form"] = avatar_form

    genders = Gender.objects.all()
    ctx["profile"] = profile
    try:
        deliverer_profile = request.user.deliverer_profile
    except:
        deliverer_profile = None

    ctx["deliverer_profile"] = deliverer_profile
    ctx["profile_birthdate"] = profile.birthdate.__str__()
    ctx["genders"] = genders
    if request.method == "POST":
        match request.POST.get("form_tag"):
            case "register":
                deliverer_profile = create_deliverer_profile(request.user)
                ctx["deliverer_profile"] = deliverer_profile
            case "avatar":
                try:
                    if request.FILES.get('avatar') == None: raise FileNotFoundError("Ảnh chưa được tải lên")
                    avatar_change(subfolders="avatars", instance=profile, file=request.FILES['avatar'])
                except Exception as e:
                    ctx["error"] = "avatar"
                    messages.error(request, message=f"{e}")
            case "profile":
                try:
                    with transaction.atomic():
                        profile.update_profile(request)
                        request.user.email = request.POST.get("email")
                        request.user.save()

                except ValidationError as e:
                    ctx["error"] = "profile"
                    match e.message:
                        case "The phone number entered is not valid.":
                            messages.error(request,
                                           message=f"Số điện thoại không hợp lệ (số điện thoại cần có đầu số của quốc gia, vd: +84)")
                        case "Enter a valid email address.":
                            messages.error(request, message=f"Email không hợp lệ")
                        case _:
                            messages.error(request, message=f"{e.message}")
                except Exception as e:
                    ctx["error"] = "profile"
                    messages.error(request, message=f"{e}")
            case "deliverer_profile":
                deliverer_profile.update_profile(request)
            case "location":
                try:
                    with transaction.atomic():
                        profile.update_location(request)
                        deliverer_profile.current_location.country = request.POST.get('country')
                        deliverer_profile.current_location.region = request.POST.get('region')
                except Exception as e:
                    ctx["error"] = "location"
                    messages.error(request, message=f"{type(e)}:{e}")
            case "update_end_time":
                print(request.POST)
                deliverer_profile.update_end_time(request)

    return render(request,"Site/DelivererProfile.html",ctx)

def CurrentLocation(request):
    if request.method == 'POST':
        request.user.deliverer_profile.update_current_location(request)
        return HttpResponse(json.dumps({
            "message": "Current location posted successfully.",
            "delivery_check": f"{request.user.deliverer_profile.current_delivery != None}"
        },indent=4),status = 200)
    return Http404()

def CheckIn(request):
    if request.method == 'POST':
        request.user.deliverer_profile.check_in(request)
        return HttpResponse(json.dumps({
            "message": "Check-in successfully."
        },indent=4),status = 200)
    return Http404()

def CurrentDeliveryView(request):
    ctx = {}
    if not request.user.is_anonymous:

        current_delivery = request.user.deliverer_profile.current_delivery
        if current_delivery:
            current_order = current_delivery.order
            ctx["current_order"] = current_order
            ctx["store_list"] = current_order.store_list
            for store in ctx["store_list"]:
                store.order_products = current_order.order_products.filter(product__store=store,status__code="submitted")
                store.total = 0
                for order_product in store.order_products:
                    store.total += order_product.total
        else:
            current_order = None
        ctx["payment_methods"] = Payment_Method.objects.all()

        if request.method == "POST":
            match request.POST.get("form_tag"):
                case "get_product":
                    current_delivery.get_product(request)
                case "get_store_products":
                    current_delivery.get_store_products(request)
                case "update_product_image":
                    current_delivery.update_product_image(request)
                case "cancel_product":
                    current_delivery.cancel_product(request)
                case "cancel_store_products":
                    current_delivery.cancel_store_products(request)
                case "dispatch":
                    current_delivery.dispatch(request)
                case "ghosted":
                    current_delivery.ghosted_report(request)

        if current_order and current_order.order_status.code != "pending" and current_order.order_status.code != "expired":
            route = current_order.delivery.points.all().order_by('priority')
            ctx["route"] = {}
            ctx["route"]["start"] = route[0]
            ctx["route"]["destination"] = route[len(route) - 1]
            ctx["route"]["stores"] = route[1:len(route) - 1]
    else:
        ctx["current_order"] = None

    return render(request, 'Site/CurrentDelivery.html', ctx)

def GetCurrentDeliveryData(request):
    ctx = {}
    if request.method == 'GET':
        if not request.user.is_anonymous:
            current_delivery = request.user.deliverer_profile.current_delivery
            current_order = current_delivery.order
            current_delivery.arrived_check()
            if current_order:
                current_order.calculate_total()
                ctx = {
                    "order_status":current_order.order_status.code,
                    "delivery_status":current_delivery.status.code,
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
