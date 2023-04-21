from django.urls import path,re_path
from products.views import *

urlpatterns = [
    path('product-list/<int:page_id>',ProductListView),
    path('product/<slug:slug>',ProductDetailView)
]