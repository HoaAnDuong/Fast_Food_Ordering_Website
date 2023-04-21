from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from profiles.models import Gender,Profile

class CustomUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
