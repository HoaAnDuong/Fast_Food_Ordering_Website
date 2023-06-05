from django.urls import path
from .views import *

urlpatterns = [
    path('store-list/<int:page_id>',StoreListView),
    path('store/<slug:slug>',StoreDetailView),
    path('current-store/',StoreView),
    path('current-store/product-list/<int:page_id>',StoreProductView),
    path('current-store/order-product/<int:page_id>',OrderProductView),
    path('current-store/latest-order-product',GetLatestOrderProduct),
    path('current-store/order-product/<int:page_id>/get-data',GetOrderProductsData),
    path('current-store/product/<slug:slug>',ProductUpdateView),
    path('current-store/product/<slug:slug>/<int:page_id>/get-reviews',GetProductReviews),
    path('current-store/product/<slug:slug>/get-statistic',GetProductStatistic),
    path('current-store/create-product',ProductCreateView)
]