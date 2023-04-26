from django.shortcuts import render
from profiles.models import *
from profiles.forms import ProfileAvatarForm
from .utils import *
from django.http import HttpResponse,Http404
import json
from foodapp.utils import avatar_change
from django.contrib import messages
from django.db import transaction
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
    print(deliverer_profile)

    ctx["deliverer_profile"] = deliverer_profile
    ctx["profile_birthdate"] = profile.birthdate.__str__()
    ctx["genders"] = genders
    if request.method == "POST":
        match request.POST.get("method_tag"):
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

            case "location":
                try:
                    with transaction.atomic():
                        profile.update_location(request)
                        deliverer_profile.current_location.country = request.POST.get('country')
                        deliverer_profile.current_location.region = request.POST.get('region')
                except Exception as e:
                    ctx["error"] = "location"
                    messages.error(request, message=f"{type(e)}:{e}")

    return render(request,"Site/DelivererProfile.html",ctx)

def CurrentLocation(request):
    if request.method == 'POST':
        request.user.deliverer_profile.update_current_location(request)
        return HttpResponse(json.dumps({
            "message": "Current location posted successfully."
        },indent=4),status = 200)
    return Http404()
