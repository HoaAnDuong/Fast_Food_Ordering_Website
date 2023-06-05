from django.urls import path
from .views import *

urlpatterns = [
    path("moderator",ModeratorView),
    path("moderator/products/<slug:slug>",ModeratedProductView),
    path("moderator/products/<slug:slug>/<int:page_id>/get-reviews",GetProductReviews),
    path("moderator/get-products/<int:page_id>",GetModeratedProduct)
]