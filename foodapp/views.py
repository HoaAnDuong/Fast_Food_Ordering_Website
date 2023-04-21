from django.shortcuts import render, redirect
from django.db import transaction
from .forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from profiles.models import Profile,User_Status,Gender
from profiles.utils import create_profile,validate_birthdate
from django.contrib.auth.models import Group
from phonenumber_field.validators import validate_international_phonenumber
from django.core.validators import validate_email
from axes.utils import reset
from django.core.exceptions import ValidationError

from django.template import RequestContext


def error_404(request, exception):
    return render(request, '404.html')

def RegistrationPage(request):
    ctx = {}
    genders = Gender.objects.all()
    ctx["genders"] = genders
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            ctx["form"] = form
            # try:
            with transaction.atomic():
                validate_birthdate(request.POST.get("birthdate"))
                validate_email(request.POST.get("email"))
                validate_international_phonenumber(request.POST.get("phone_number"))
                form.save()

                username = request.POST.get('username')
                password = request.POST.get('password1')
                email = request.POST.get('email')

                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                gender_id = request.POST.get("gender")
                birthdate = request.POST.get("birthdate")
                phone_number = request.POST.get("phone_number")

                user = authenticate(request, username=username, password=password, email=email)
                user.groups.add(Group.objects.get(name="Customers"))
                create_profile(user,first_name=first_name,last_name=last_name,
                               gender_id=gender_id,birthdate=birthdate,phone_number=phone_number,email=email)
                return redirect('/login')
            # except ValidationError as e:
            #     ctx["error"] = "profile"
            #     match e.message:
            #         case "The phone number entered is not valid.":
            #             messages.error(request,
            #                            message=f"Số điện thoại không hợp lệ (số điện thoại cần có đầu số của quốc gia, vd: +84)")
            #         case "Enter a valid email address.":
            #             messages.error(request,
            #                            message=f"Email không hợp lệ")
            #         case _:
            #             messages.error(request, message=f"{e.message}")
            # except Exception as e:
            #     ctx["error"] = "profile"
            #     messages.error(request, message=f"{type(e)}:{e}")
        else:
            ctx["form"] = form
    else:
        form = CustomUserForm()
        ctx["form"] = form
    return render(request,'Site/Register.html',ctx)


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            reset(username=username)
        else:
            messages.info(request,message="User and/or password are incorrect")
    ctx = {"active_link":"login"}
    return render(request,'Site/Login.html',ctx)

def LogoutPage(request):
    if not request.user.is_anonymous:
        if request.method == 'POST':
            logout(request)
    return render(request,'Site/Logout.html')

def Home(request):
    return render(request,'Site/Home.html')

def RouteTest(request):
    return render(request,'Site/RoutingTest.html')

