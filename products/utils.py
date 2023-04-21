from .models import Product
from django.contrib.auth.models import Group

def recommended_products(user,location = None,*args,**kwargs):
    if user.is_anonymous:
        return Product.objects.all()
    else:
        products = Product.objects.all().exclude(store__user=user).filter(store__status__code = "active")
    for p in products:
        if user.profile.current_order != None:
            p.distance = p.store.distance_to(user.profile.current_order.destination)
        else:
            p.distance = p.store.distance_to(user.profile.location)
    return products