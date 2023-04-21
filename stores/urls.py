from django.urls import path
from .views import *

urlpatterns = [
    path('',StoreView),
    path('product-list/<int:page_id>',StoreProductView),
    path('order-product/<int:page_id>',OrderProductView),
]