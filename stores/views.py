from django.shortcuts import render
from .utils import *
from foodapp.utils import avatar_change
from django.contrib import messages
from django.db import transaction
from stores.models import Store_Opening_Hours,Store
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.core.paginator import Paginator
from orders.models import Order_Product
from products.models import *
from django.http import HttpResponse,Http404
import json
from django.db.models import Q
import calendar
from django.views.decorators.csrf import csrf_protect
from django.db.models import Avg,Count,Sum
from .utils import recommended_stores
from products.utils import recommended_products
# Create your views here.

def StoreDetailView(request,slug):
    ctx = {}
    store = Store.objects.get(slug = slug)
    ctx["store"] = store
    ctx["recommended_products"] = recommended_products(user=request.user)[:10]
    ctx["store_products"] = Product.objects.filter(store = store)

    return render(request, 'Site/StoreDetail.html',ctx)

def StoreListView(request,page_id=1):

    product = recommended_stores(request)
    paginator = Paginator(product, 20)
    page = paginator.get_page(page_id)
    return StoreBaseListView(request,paginator,page,{})
def StoreBaseListView(request,paginator,page,ctx):
    ctx = ctx

    ctx["page"] = page
    ctx["page_range"] = range(1,paginator.num_pages+1)

    return render(request,'Site/StoreList.html',ctx)

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
    products = Product.objects.filter(store = store)
    paginator = Paginator(products, 10)
    page = paginator.get_page(page_id)
    ctx["page"] = page
    ctx["page_range"] = range(1, paginator.num_pages + 1)

    if request.method == "POST":
        match request.POST.get("form_tag"):
            case "delete_product":
                product = page[int(request.POST.get("id"))]
                product.delete_product()
            case "disable_product":
                product = page[int(request.POST.get("id"))]
                product.disable_product()
            case "active_product":
                product = page[int(request.POST.get("id"))]
                product.active_product()

    return render(request, "Site/StoreProductList.html", ctx)
def ProductUpdateView(request,slug):
    ctx = {}
    try:
        store = request.user.store
    except:
        store = None
    product = Product.objects.get(store=store,slug=slug)
    categories = Category.objects.all()
    ctx["product"] = product
    ctx["categories"] = categories

    reviews = Product_Review.objects.filter(product__slug = slug)
    paginator = Paginator(reviews, 10)
    ctx["page_range"] = range(1, paginator.num_pages + 1) if len(reviews) != 0 else None

    if request.method == "POST":
        match request.POST.get("form_tag"):
            case "image_upload":
                product.image_upload(request)
            case "product_update":
                product.update_product(request)



    return render(request, "Site/ProductUpdate.html", ctx)

def GetProductStatistic(request,slug):
    ctx = {}
    if request.method == "POST":
        if request.user.profile.is_store_owner:
            product = Product.objects.get(slug=slug,store=request.user.store)
            match request.POST.get('statistic_tag'):
                case "hour":
                    selected_date = datetime.datetime.fromisoformat(request.POST.get('statistic_data')).date()

                    order_products = Order_Product.objects.filter(product=product,updated = selected_date).exclude(status__code="pending")
                    completed_order_product = order_products.exclude(Q(status__code="submitted")|Q(status__code="cancelled")|Q(status__code="ghosted"))

                    store_order_products = Order_Product.objects.filter(updated=selected_date).exclude(
                        status__code="pending")
                    store_completed_order_product = store_order_products.exclude(
                        Q(status__code="submitted") | Q(status__code="cancelled") | Q(status__code="ghosted"))

                    ctx["statistic"] = {
                        "completed":{
                            "store_total": store_completed_order_product.aggregate(Sum('total'))["total__sum"],
                            "total": completed_order_product.aggregate(Sum('total'))["total__sum"],
                            "store_order_count": store_completed_order_product.aggregate(Count('order'))["order__count"],
                            "order_count": completed_order_product.aggregate(Count('order'))["order__count"],
                            "quantity":completed_order_product.aggregate(Sum('quantity'))["quantity__sum"]
                        },
                        "submitted":{
                            "store_total": store_order_products.filter(status__code="submitted").aggregate(Sum('total'))[
                                "total__sum"],
                            "total":order_products.filter(status__code="submitted").aggregate(Sum('total'))["total__sum"],
                            "store_order_count": store_order_products.filter(status__code="submitted").aggregate(Count('order'))[
                                "order__count"],
                            "order_count":order_products.filter(status__code="submitted").aggregate(Count('order'))["order__count"],
                            "quantity": order_products.filter(status__code="submitted").aggregate(Sum('quantity'))[
                                "quantity__sum"]
                        },
                        "cancelled": {
                            "store_total": store_order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Sum('total'))["total__sum"],
                            "total": order_products
                            .filter(Q(status__code="cancelled")|Q(status__code="ghosted"))
                            .aggregate(Sum('total'))["total__sum"],
                            "store_order_count": store_order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Count('order'))["order__count"],
                            "order_count": order_products
                            .filter(Q(status__code="cancelled")|Q(status__code="ghosted"))
                            .aggregate(Count('order'))["order__count"],
                            "quantity": order_products
                            .filter(Q(status__code="cancelled")|Q(status__code="ghosted"))
                            .aggregate(Sum('quantity'))["quantity__sum"],
                        }
                    }

                    ctx["data"] = [
                        {
                            "completed":{
                                "total":completed_order_product.filter(updated__hour = hour).aggregate(Sum('total'))["total__sum"],
                                "order_count":completed_order_product.filter(updated__hour = hour).aggregate(Count('order'))["order__count"],
                                "quantity": completed_order_product.filter(updated__hour=hour).aggregate(Sum('quantity'))["quantity__sum"],
                            },
                            "submitted":{
                                "total":order_products.filter(updated__hour = hour,status__code="submitted").aggregate(Sum('total'))["total__sum"],
                                "order_count":order_products.filter(updated__hour = hour,status__code="submitted").aggregate(Count('order'))["order__count"],
                                "quantity":order_products.filter(updated__hour = hour,status__code="submitted").aggregate(Sum('quantity'))["quantity__sum"],
                            },
                            "cancelled": {
                                "total": order_products.filter(updated__hour=hour)
                                .filter(Q(status__code="cancelled")|Q(status__code="ghosted"))
                                .aggregate(Sum('total'))["total__sum"],
                                "order_count": order_products.filter(updated__hour=hour)
                                .filter(Q(status__code="cancelled")|Q(status__code="ghosted"))
                                .aggregate(Count('order'))["order__count"],
                                "quantity": order_products.filter(updated__hour=hour)
                                .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                                .aggregate(Sum('quantity'))["quantity__sum"],
                            }
                        }
                        for hour in range(24)
                    ]
                case "day":
                    selected_date = datetime.datetime.fromisoformat(request.POST.get('statistic_data')).date()
                    order_products = Order_Product.objects.filter(product=product,
                                                                  updated__month = selected_date.month,updated__year = selected_date.year).exclude(
                        status__code="pending")
                    completed_order_product = order_products.exclude(
                        Q(status__code="submitted") | Q(status__code="cancelled") | Q(status__code="ghosted"))

                    store_order_products = Order_Product.objects.filter(updated__month = selected_date.month,updated__year = selected_date.year).exclude(
                        status__code="pending")
                    store_completed_order_product = store_order_products.exclude(
                        Q(status__code="submitted") | Q(status__code="cancelled") | Q(status__code="ghosted"))

                    ctx["statistic"] = {
                        "completed": {
                            "store_total": store_completed_order_product.aggregate(Sum('total'))["total__sum"],
                            "total": completed_order_product.aggregate(Sum('total'))["total__sum"],
                            "store_order_count": store_completed_order_product.aggregate(Count('order'))[
                                "order__count"],
                            "order_count": completed_order_product.aggregate(Count('order'))["order__count"],
                            "quantity": completed_order_product.aggregate(Sum('quantity'))["quantity__sum"]
                        },
                        "submitted": {
                            "store_total":
                                store_order_products.filter(status__code="submitted").aggregate(Sum('total'))[
                                    "total__sum"],
                            "total": order_products.filter(status__code="submitted").aggregate(Sum('total'))[
                                "total__sum"],
                            "store_order_count":
                                store_order_products.filter(status__code="submitted").aggregate(Count('order'))[
                                    "order__count"],
                            "order_count": order_products.filter(status__code="submitted").aggregate(Count('order'))[
                                "order__count"],
                            "quantity": order_products.filter(status__code="submitted").aggregate(Sum('quantity'))[
                                "quantity__sum"]
                        },
                        "cancelled": {
                            "store_total": store_order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Sum('total'))["total__sum"],
                            "total": order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Sum('total'))["total__sum"],
                            "store_order_count": store_order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Count('order'))["order__count"],
                            "order_count": order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Count('order'))["order__count"],
                            "quantity": order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Sum('quantity'))["quantity__sum"],
                        }
                    }

                    ctx["data"] = [
                        {
                            "completed": {
                                "total": completed_order_product.filter(updated__day=day).aggregate(Sum('total'))[
                                    "total__sum"],
                                "order_count": completed_order_product.filter(updated__day=day).aggregate(Count('order'))[
                                    "order__count"],
                                "quantity": completed_order_product.filter(updated__day=day).aggregate(Sum('quantity'))["quantity__sum"]
                            },
                            "submitted": {
                                "total": order_products.filter(updated__day=day, status__code="submitted").aggregate(
                                    Sum('total'))["total__sum"],
                                "order_count": order_products.filter(updated__day=day, status__code="submitted").aggregate(
                                    Count('order'))["order__count"],
                                "quantity": order_products.filter(status__code="submitted").aggregate(Sum('quantity'))[
                                    "quantity__sum"]
                            },
                            "cancelled": {
                                "total": order_products.filter(updated__day=day)
                                .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                                .aggregate(Sum('total'))["total__sum"],
                                "order_count": order_products.filter(updated__day=day)
                                .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                                .aggregate(Count('order'))["order__count"],
                                "quantity": order_products.filter(updated__day=day)
                                .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                                .aggregate(Sum('quantity'))["quantity__sum"]
                            }
                        }
                        for day in range(1, calendar.monthrange(selected_date.year,selected_date.month)[1])
                    ]
                case "month":
                    selected_year = request.POST.get('statistic_data')
                    order_products = Order_Product.objects.filter(product=product,
                                                                  updated__year=selected_year).exclude(
                        status__code="pending")
                    completed_order_product = order_products.exclude(
                        Q(status__code="submitted") | Q(status__code="cancelled") | Q(status__code="ghosted"))

                    store_order_products = Order_Product.objects.filter(updated__year=selected_year).exclude(
                        status__code="pending")
                    store_completed_order_product = store_order_products.exclude(
                        Q(status__code="submitted") | Q(status__code="cancelled") | Q(status__code="ghosted"))

                    ctx["statistic"] = {
                        "completed": {
                            "store_total": store_completed_order_product.aggregate(Sum('total'))["total__sum"],
                            "total": completed_order_product.aggregate(Sum('total'))["total__sum"],
                            "store_order_count": store_completed_order_product.aggregate(Count('order'))[
                                "order__count"],
                            "order_count": completed_order_product.aggregate(Count('order'))["order__count"],
                            "quantity": completed_order_product.aggregate(Sum('quantity'))["quantity__sum"]
                        },
                        "submitted": {
                            "store_total":
                                store_order_products.filter(status__code="submitted").aggregate(Sum('total'))[
                                    "total__sum"],
                            "total": order_products.filter(status__code="submitted").aggregate(Sum('total'))[
                                "total__sum"],
                            "store_order_count":
                                store_order_products.filter(status__code="submitted").aggregate(Count('order'))[
                                    "order__count"],
                            "order_count": order_products.filter(status__code="submitted").aggregate(Count('order'))[
                                "order__count"],
                            "quantity": order_products.filter(status__code="submitted").aggregate(Sum('quantity'))[
                                "quantity__sum"]
                        },
                        "cancelled": {
                            "store_total": store_order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Sum('total'))["total__sum"],
                            "total": order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Sum('total'))["total__sum"],
                            "store_order_count": store_order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Count('order'))["order__count"],
                            "order_count": order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Count('order'))["order__count"],
                            "quantity": order_products
                            .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                            .aggregate(Sum('quantity'))["quantity__sum"],
                        }
                    }

                    ctx["data"] = [
                        {
                            "completed": {
                                "total": completed_order_product.filter(updated__month=month).aggregate(Sum('total'))[
                                    "total__sum"],
                                "order_count": completed_order_product.filter(updated__month=month).aggregate(Count('order'))[
                                    "order__count"],
                                "quantity": completed_order_product.filter(updated__month=month).aggregate(Sum('quantity'))["quantity__sum"]
                            },
                            "submitted": {
                                "total": order_products.filter(updated__month=month, status__code="submitted").aggregate(
                                    Sum('total'))["total__sum"],
                                "order_count":
                                    order_products.filter(updated__month=month, status__code="submitted").aggregate(
                                        Count('order'))["order__count"],
                                "quantity": order_products.filter(status__code="submitted").aggregate(Sum('quantity'))[
                                    "quantity__sum"]
                            },
                            "cancelled": {
                                "total": order_products.filter(updated__month=month)
                                .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                                .aggregate(Sum('total'))["total__sum"],
                                "order_count": order_products.filter(updated__month=month)
                                .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                                .aggregate(Count('order'))["order__count"],
                                "quantity": order_products.filter(updated__month=month)
                                .filter(Q(status__code="cancelled") | Q(status__code="ghosted"))
                                .aggregate(Sum('quantity'))["quantity__sum"]
                            }
                        }
                        for month in range(1, 13)
                    ]

            for item in ctx["statistic"].items():
                print(item)
                item[1]["total"] = float(item[1]["total"]) if item[1]["total"] else 0
                item[1]["quantity"] = int(item[1]["quantity"]) if item[1]["quantity"] else 0
                item[1]["order_count"] = int(item[1]["order_count"]) if item[1]["order_count"] else 0
                item[1]["store_total"] = float(item[1]["total"]) if item[1]["total"] else 0
                item[1]["store_order_count"] = int(item[1]["store_order_count"]) if item[1]["store_order_count"] else 0

            for item in ctx["data"]:
                for subitem in item.items():
                    subitem[1]["total"] = float(subitem[1]["total"]) if subitem[1]["total"] else 0
                    subitem[1]["quantity"] = int(subitem[1]["quantity"]) if subitem[1]["quantity"] else 0

            return HttpResponse(json.dumps(ctx), status=200)
    else:
        return Http404()

def GetProductReviews(request,slug,page_id):
    ctx = {}
    if request.method == "POST":
        if request.user.profile.is_store_owner:
            store = request.user.store
            reviews = Product_Review.objects.filter(product__slug = slug,product__store=store)

            ctx["statistic"] = [
                len(reviews.filter(rating=5)),
                len(reviews.filter(rating=4.5)),
                len(reviews.filter(rating=4)),
                len(reviews.filter(rating=3.5)),
                len(reviews.filter(rating=3)),
                len(reviews.filter(rating=2.5)),
                len(reviews.filter(rating=2)),
                len(reviews.filter(rating=1.5)),
                len(reviews.filter(rating=1)),
                len(reviews.filter(rating=0.5)),
                len(reviews.filter(rating=0))
            ]

            filtered_name = request.POST.get('filtered_author')
            filtered_rating = float(request.POST.get('filtered_rating')) if request.POST.get(
                'filtered_rating') else None

            if filtered_name:
                word_list = filtered_name.split()
                if len(word_list) == 0: word_list = [""]
                search_query = (Q(author__profile__first_name__contains=word_list[0]) | Q(
                    author__profile__last_name__contains=word_list[0]))
                for i in range(1, len(word_list)):
                    search_query = search_query & (Q(author__profile__first_name__contains=word_list[i]) | Q(
                        author__profile__last_name__contains=word_list[i]))
                reviews = reviews.filter(search_query)

            if filtered_rating:
                reviews = reviews.filter(rating=filtered_rating)


            paginator = Paginator(reviews, 10)
            page = paginator.get_page(page_id)
            ctx["page_id"] = page.number
            ctx["num_pages"] = paginator.num_pages
            ctx["reviews"] = [
                {
                    "avatar_url" : review.author.profile.avatar.url,
                    "author_name": f"{review.author.profile.last_name} {review.author.profile.first_name}",
                    "updated": review.updated.__str__(),
                    "is_updated": review.is_updated,
                    "rating": review.rating,
                    "title": review.title,
                    "review": review.review,
                    "image_url": review.image.url if review.image else None,
                    "id":review.id
                }
                for review in page
            ]

        return HttpResponse(json.dumps(ctx), status=200)
    else:
        return Http404()
@csrf_protect
def ProductCreateView(request):
    ctx = {}
    store = request.user.store
    if request.method == "POST":
        match request.POST.get("form_tag"):
            case "create_product":
                selected_category = Category.objects.get(id = request.POST.get("category_id"))
                store.create_product(request,Product_Status.objects.get(code = "pending"),selected_category)
    categories = Category.objects.all()
    ctx["categories"] = categories
    return render(request,"Site/ProductCreate.html",ctx)

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

def GetOrderProductsData(request,page_id):
    ctx = {}
    if request.method == "POST":
        if request.user.profile.is_store_owner:
            try:
                with transaction.atomic():
                    store = request.user.store
                    order_products = Order_Product.objects.exclude(status__code="pending").filter(product__store=store).order_by(
                        "-updated")
            except:
                return HttpResponse(status=400)
        paginator = Paginator(order_products, 10)
        page = paginator.get_page(page_id)
        ctx = {
            "page_id":page_id,
            'num_submitted_product':len(order_products.filter(created__date=datetime.datetime.now().date())),
            "order_product":[
                {
                    "name":order_product.product.name,
                    "image_url":order_product.product.image.url,
                    'quantity':order_product.quantity,
                    'price':order_product.price.__str__(),
                    'total':order_product.total.__str__(),
                    'created':order_product.created.__str__(),
                    'updated':order_product.updated.__str__(),
                    'status':order_product.status.code,
                    'address':order_product.order.destination.address,
                    'slug':order_product.product.slug
                }
                for order_product in page
            ]
        }
        match request.POST.get('statistic_tag'):
            case "hour":
                selected_date = datetime.datetime.fromisoformat(request.POST.get('statistic_data')).date()
                ctx["statistic_tag"] = "hour"
                ctx["statistic"] = [
                    {
                        "submitted":len(order_products.filter(updated__date=selected_date,
                                                          updated__hour = hour,status__code="submitted")),
                        "cancelled":len(order_products.filter(updated__date=selected_date,
                                                          updated__hour = hour,).filter(Q(status__code="cancelled")|Q(status__code="ghosted"))),
                        "completed":len(order_products.filter(updated__date=selected_date,
                                                          updated__hour = hour).exclude(status__code = "submitted").exclude(Q(status__code="cancelled")|Q(status__code="ghosted")))
                    }
                                    for hour in range(0,24)]
            case "day":
                selected_date = datetime.datetime.fromisoformat(request.POST.get('statistic_data')).date()
                ctx["statistic_tag"] = "day"
                ctx["statistic"] = [
                    {
                        "submitted": len(order_products.filter(updated__year=selected_date.year,
                                                               updated__month=selected_date.month,
                                                               updated__day = day,
                                                               status__code="submitted")),
                        "cancelled": len(order_products.filter(updated__year=selected_date.year,
                                                               updated__month=selected_date.month,
                                                               updated__day = day).filter(
                            Q(status__code="cancelled") | Q(status__code="ghosted"))),
                        "completed": len(order_products.filter(updated__year=selected_date.year,
                                                               updated__month=selected_date.month,
                                                               updated__day = day).exclude(status__code="submitted").exclude(
                            Q(status__code="cancelled") | Q(status__code="ghosted")))
                    }
                    for day in range(1, calendar.monthrange(selected_date.year,selected_date.month)[1])]
            case "month":
                selected_year = request.POST.get('statistic_data')
                ctx["statistic_tag"] = "month"
                ctx["statistic"] = [
                    {
                        "submitted": len(order_products.filter(updated__year=selected_year,
                                                               updated__month= month,
                                                               status__code="submitted")),
                        "cancelled": len(order_products.filter(updated__year=selected_year,
                                                               updated__month= month,).filter(
                            Q(status__code="cancelled") | Q(status__code="ghosted"))),
                        "completed": len(order_products.filter(updated__year=selected_year,
                                                               updated__month= month,).exclude(
                            status__code="submitted").exclude(
                            Q(status__code="cancelled") | Q(status__code="ghosted")))
                    }
                    for month in range(1, 13)]


        return HttpResponse(json.dumps(ctx), status=200)
    else:
        return Http404()


def GetLatestOrderProduct(request):
    pass
    ctx = {}
    if request.method == 'POST':
        if request.user.profile.is_store_owner:
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
                    "quantity":order_product.quantity,
                    "price":order_product.price.__str__(),
                    "status":order_product.status.code,
                    "updated":order_product.updated.__str__()
                }
                return HttpResponse(json.dumps(ctx), status=200)
            return HttpResponse(status=400)
    else:
        return Http404()