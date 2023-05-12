from .models import Product
from django.contrib.auth.models import Group
from django.db.models import Count, F, Value, Q, Avg
from foodapp.settings import MAX_DISTANCE
import math

def recommended_products(user,*args,**kwargs):
    if user.is_anonymous:
        return Product.objects.filter(store__status__code = "active")

    else:
        if user.profile.current_order!=None:
            current_location = user.profile.current_order.destination
        else:
            current_location = user.profile.location

        products = Product.objects.all().exclude(store__user=user) \
                    .filter(store__status__code = "active") \
                    .annotate(distance=(((F("store__location__lat") - current_location.lat) ** 2.
                                        + (F("store__location__lng") - current_location.lng) ** 2.)
                                       ** 0.5 * 111.319)) \
                    .filter(distance__lte=2*MAX_DISTANCE)
    for p in products:
        p.distance = round(p.distance,ndigits=2)
    return products

def searched_products(user,search_keyword,*args,**kwargs):
    keyword_list = search_keyword.split()
    if len(keyword_list) == 0: keyword_list = [""]
    search_query = Q(name__contains=keyword_list[0])
    for i in range(1,len(keyword_list)):
        search_query = search_query & Q(name__contains=keyword_list[i])
    if user.is_anonymous:
        return Product.objects.filter(store__status__code = "active") \
                                .filter(search_query)
    else:
        if user.profile.current_order!=None:
            current_location = user.profile.current_order.destination
        else:
            current_location = user.profile.location

        products = Product.objects.all().exclude(store__user=user)\
                    .filter(store__status__code = "active") \
                    .filter(search_query)\
                    .annotate(distance=(((F("store__location__lat") - current_location.lat) ** 2.
                                        + (F("store__location__lng") - current_location.lng) ** 2.)
                                       ** 0.5 * 111.319)) \
                    .filter(distance__lte=2*MAX_DISTANCE) \
                    .order_by('distance')
    for p in products:
        p.distance = round(p.distance,ndigits=2)
    return products