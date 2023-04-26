from django.urls import path
from .views import *

urlpatterns = [
    path('current-order/',CurrentOrderView),
    path('current-order/get-data',GetCurrentOrderData),
    path('current-order/deliverer-location',DelivererCurrentLocation)
]