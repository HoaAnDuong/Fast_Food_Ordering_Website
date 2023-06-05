from django.urls import path
from .views import *

urlpatterns = [
    path('profile/',ProfileView),
    path('profile/orders/<int:page_id>',OrderView),
    path('profile/order-list',OrderListView),
    path('profile/order-list/<int:page_id>/get-data',GetOrderListData)
]