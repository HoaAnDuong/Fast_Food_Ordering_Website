from django.shortcuts import render
from django.db import transaction
from django.contrib import messages
from .forms import ProfileAvatarForm
from .utils import *
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from .models import Profile,Gender,User_Status
from foodapp.utils import avatar_change
from orders.models import Order,Payment_Method
import os
from django.core.paginator import Paginator

# Create your views here.


def ProfileView(request):
    ctx = {}
    profile = Profile.objects.get(user=request.user)

    avatar_form = ProfileAvatarForm(instance=profile)
    ctx["avatar_form"] = avatar_form

    genders = Gender.objects.all()
    ctx["profile"] = profile
    ctx["profile_birthdate"] = profile.birthdate.__str__()
    ctx["genders"] = genders

    if request.method == "POST":
        print(request.POST)

        match request.POST.get("form_tag"):
            case "avatar":
                try:
                    if request.FILES.get('avatar') == None: raise FileNotFoundError("Ảnh chưa được tải lên")
                    avatar_change(subfolders="avatars",instance=profile,file = request.FILES['avatar'])
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
                            messages.error(request,message=f"Số điện thoại không hợp lệ (số điện thoại cần có đầu số của quốc gia, vd: +84)")
                        case "Enter a valid email address.":
                            messages.error(request,message=f"Email không hợp lệ")
                        case _:
                            messages.error(request, message=f"{e.message}")
                except Exception as e:
                    ctx["error"] = "profile"
                    messages.error(request, message = f"{e}")

            case "location":
                try:
                    with transaction.atomic():
                        profile.update_location(request)

                except Exception as e:
                    ctx["error"] = "location"
                    messages.error(request, message=f"{type(e)}:{e}")

            case "change_password":
                profile.change_password(request)
                ctx["password_changed"] = True
        profile = Profile.objects.get(user=request.user)
        ctx["profile"] = profile

    return render(request,"Site/Profile.html",ctx)

def OrderView(request,page_id):
    ctx = {}
    current_order = Order.objects.filter(customer = request.user).order_by('-updated')[page_id - 1]
    ctx["remain_cancellations"] = request.user.profile.remain_cancellations
    ctx["current_order"] = current_order
    ctx["payment_methods"] = Payment_Method.objects.all()
    if current_order and current_order.order_status.code != "pending" and current_order.order_status.code != "expired":
        route = current_order.delivery.points.all().order_by('priority')

        ctx["route"] = {}
        ctx["route"]["start"] = route[0]
        ctx["route"]["destination"] = route[len(route) - 1]
        ctx["route"]["stores"] = route[1:len(route) - 1]
    return render(request, "Site/OrderView.html", ctx)
def OrderListView(request):
    ctx = {}
    orders = Order.objects.filter(customer = request.user).order_by('-updated')
    paginator = Paginator(orders, 10)
    ctx["page_range"] = range(1, paginator.num_pages + 1) if len(orders) != 0 else None
    return render(request, "Site/OrderView.html",ctx)