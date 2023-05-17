from django.urls import path
from .views import *

urlpatterns = [
    path('',StoreView),
    path('product-list/<int:page_id>',StoreProductView),
    path('order-product/<int:page_id>',OrderProductView),
    path('latest-order-product',GetLatestOrderProduct),
    path('order-product/<int:page_id>/get-data',GetOrderProductsData),
    path('product/<slug:slug>',ProductUpdateView),
    path('product/<slug:slug>/<int:page_id>/get-reviews',GetProductReviews),
    path('create-product',ProductCreateView)
]