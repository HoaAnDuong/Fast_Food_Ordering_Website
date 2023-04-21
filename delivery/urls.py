from django.urls import path
from .views import *

urlpatterns = [
    path('current-location',CurrentLocation),
    path('deliverer-profile/',DelivererProfileView),
]