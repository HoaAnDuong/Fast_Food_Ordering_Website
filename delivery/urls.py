from django.urls import path
from .views import *

urlpatterns = [
    path('check-in',CheckIn),
    path('current-location',CurrentLocation),
    path('deliverer-profile/',DelivererProfileView),
    path('current-delivery',CurrentDeliveryView),
    path('current-delivery/get-data',GetCurrentDeliveryData)
]