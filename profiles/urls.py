from django.urls import path
from .views import *

urlpatterns = [
    path('profile/',ProfileView),
    path('profile/orders/<int:page_id>',OrderView)
]