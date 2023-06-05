from django.urls import path
from .views import *

urlpatterns = [
    path('check-in',CheckIn),
    path('current-location',CurrentLocation),
    path('deliverer-profile/',DelivererProfileView),
    path('deliverer-profile/delivery-list',DeliveryListView),
    path('deliverer-profile/delivery-list/<int:page_id>/get-data',GetDelivererListData),
    path('deliverer-profile/deliveries/<int:page_id>',DeliveryView),
    path('current-delivery',CurrentDeliveryView),
    path('current-delivery/get-data',GetCurrentDeliveryData)
]