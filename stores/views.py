from django.shortcuts import render
from .utils import *
from foodapp.utils import avatar_change
from django.contrib import messages
from django.db import transaction
from stores.models import Store_Opening_Hours,Store
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.core.paginator import Paginator
from orders.models import Order_Product
from products.models import Product
from django.http import HttpResponse,Http404
import json

# Create your views here.

def StoreView(request):
    ctx = {}
    try:
        store = request.user.store
    except:
        store = None
    if store != None and store.location == None:
        store.location = Location.objects.create()
    ctx["store"] = store
    ctx["opening_hours"] = {}

    if request.method == "POST":
        match request.POST.get("form_tag"):
            case "register":
                ctx["store"] = create_pending_store(request.user)
            case "avatar":
                try:
                    if request.FILES.get('avatar') == None: raise FileNotFoundError("Ảnh chưa được tải lên")
                    print(request.FILES.get('avatar').__dict__)
                    avatar_change(subfolders="stores",instance=store,file = request.FILES['avatar'])
                except Exception as e:
                    ctx["error"] = "avatar"
                    messages.error(request, message=f"{e}")
            case "store":
                try:
                    with transaction.atomic():
                        store.update_store(request)
                except Exception as e:
                    ctx["error"] = "store"
                    messages.error(request, message=f"{e}")
            case "location":
                try:
                    with transaction.atomic():
                        store.update_location(request)

                except Exception as e:
                    ctx["error"] = "location"
                    messages.error(request, message=f"{type(e)}:{e}")
            case "opening_hours":
                for i in range(7):
                    try:
                        try:
                            opening_hours = store.opening_hours.get(weekday=i)
                        except ObjectDoesNotExist as e:
                            opening_hours = Store_Opening_Hours.objects.create(store=store, weekday=i)

                        opening_hours.update(str_from_hour = request.POST.get(f'from_hour_{i}'),
                                             str_to_hour = request.POST.get(f'to_hour_{i}'))
                        request.user.store.save()
                    except ValidationError as e:
                        ctx["error"] = "opening_hours"
                        messages.error(request, message= f"{e.message}")
                    except Exception as e:
                        ctx["error"] = "opening_hours"
                        messages.error(request, message=f"{type(e)}:{e}")
            case "opening_hours_all":
                for i in range(7):
                    try:
                        try:
                            opening_hours = store.opening_hours.get(weekday=i)
                        except ObjectDoesNotExist as e:
                            opening_hours = Store_Opening_Hours.objects.create(store=store, weekday=i)

                        opening_hours.update(str_from_hour=request.POST.get('from_hour_all'),
                                             str_to_hour=request.POST.get('to_hour_all'))
                        request.user.store.save()
                    except ValidationError as e:
                        ctx["error"] = "opening_hours"
                        messages.error(request, message=f"{e.message}")
                    except Exception as e:
                        ctx["error"] = "opening_hours"
                        messages.error(request, message=f"{type(e)}:{e}")

    for i in range(7):
        try:
            from_hour = store.opening_hours.get(weekday=i).from_hour
            from_hour = from_hour.strftime("%H:%M")
            to_hour = store.opening_hours.get(weekday=i).to_hour
            to_hour = to_hour.strftime("%H:%M")
            ctx["opening_hours"][i] = {}
            ctx["opening_hours"][i]["from_hour"] = from_hour
            ctx["opening_hours"][i]["to_hour"] = to_hour
        except:
            ctx["opening_hours"][i] = None

    return render(request,"Site/Store.html",ctx)

def StoreProductView(request,page_id):
    ctx = {}
    try:
        store = request.user.store
    except:
        store = None
    product = Product.objects.filter(store = store)
    paginator = Paginator(product, 10)
    page = paginator.get_page(page_id)
    ctx["page"] = page
    ctx["page_range"] = range(1, paginator.num_pages + 1)

    return render(request, "Site/StoreProductList.html", ctx)

def OrderProductView(request,page_id):
    ctx = {}
    try:
        store = request.user.store
    except:
        store = None
    if store != None:

        order_products = Order_Product.objects.exclude(status__code="pending").filter(product__store = store).order_by("-updated")

        paginator = Paginator(order_products, 10)
        page = paginator.get_page(page_id)
        ctx["page"] = page
        ctx["page_range"] = range(1, paginator.num_pages + 1)
        if request.method == "POST":
            match request.POST.get("form_tag"):
                case "cancel_product":
                    selected_order_product = page[int(request.POST.get("id"))]
                    selected_order_product.cancel()
                    selected_order_product.order.logs.create(
                        log=f"{datetime.datetime.now()}: Món {selected_order_product.product.name} với số lượng {selected_order_product.quantity} đã bị hủy từ phía cửa hàng")


    return render(request, "Site/StoreOrderProduct.html", ctx)

def GetLatestOrderProduct(request):
    pass
    ctx = {}
    if request.method == 'POST':
        if request.user.is_store_owner:
            try:
                with transaction.atomic():
                    store = request.user.store
                    order_product = Order_Product.objects\
                                            .exclude(status__code="pending")\
                                            .filter(product__store=store).order_by("-updated")[0]
            except:
                return HttpResponse(status=400)

            if order_product:
                ctx = {
                    "product_name":order_product.product.name,
                    "quantity":order_product.product.quantity,
                    "price":order_product.price,
                    "status":order_product.status,
                    "updated":order_product.updated
                }
                return HttpResponse(json.dumps(ctx), status=200)
            return HttpResponse(status=400)
    else:
        return Http404()