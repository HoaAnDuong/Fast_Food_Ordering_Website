from django.shortcuts import render
from .utils import *
from .models import *
from django.db import transaction
from django.contrib import messages


# Create your views here.

def CurrentOrderView(request):
    ctx = {}
    if not request.user.is_anonymous:
        current_order_expire_check(request.user)
        current_order = request.user.profile.current_order
        ctx["current_order"] = current_order
        if current_order:
            ctx["store_list"] = current_order.store_list
        ctx["payment_methods"] = Payment_Method.objects.all()
        if request.method == "POST":
            match request.POST.get("method_tag"):
                case "create_order":
                    create_new_order(request.user)
                case "update_order":
                    current_order.payment_method = Payment_Method.objects.get(id = request.POST.get("payment_method"))
                    current_order.save()
                case "location":
                    try:
                        with transaction.atomic():
                            current_order.update_location(request)
                            current_order.destination.save()
                    except Exception as e:
                        ctx["error"] = "location"
                        messages.error(request, message=f"{type(e)}:{e}")

                case "update_product":
                    product = Product.objects.get(id=request.POST.get("product_id"))
                    current_order.update_product(product,quantity=request.POST.get("quantity"),note=request.POST.get("note"))

                case "delete_product":
                    product = Product.objects.get(id=request.POST.get("product_id"))
                    current_order.delete_product(product)
            current_order = request.user.profile.current_order
            ctx["current_order"] = current_order
    else:
        ctx["current_order"] = None

    return render(request, 'Site/CurrentOrder.html', ctx)
