"""foodapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from products.views import ProductListView
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('products.urls')),
    path('',include('profiles.urls')),
    path('',include('stores.urls')),
    path('',include('orders.urls')),
    path('',include('delivery.urls')),
    path('',include('moderating.urls')),
    path('',Home),
    path('login',LoginPage),
    path('register',RegistrationPage),
    path('routing-test',RouteTest),
    path('logout',LogoutPage),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
