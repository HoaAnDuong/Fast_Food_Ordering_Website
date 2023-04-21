from django.shortcuts import render
from profiles.models import *
from profiles.forms import ProfileAvatarForm
from .utils import *
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

    return render(request,"Site/DelivererProfile.html",ctx)

def CurrentLocation(request):
    if request.method == 'POST':
        print(request.POST)
