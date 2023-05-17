from django.shortcuts import render,redirect
from django.views import generic
from orders.utils import current_order_expire_check,create_new_order
from django.core.paginator import Paginator
from .utils import recommended_products,searched_products
from django.core.exceptions import ValidationError,ObjectDoesNotExist

from .models import *

# class ProductListView(generic.ListView):
#     model = Product
#     template_name = 'Site/ProductList.html'
# class ProductDetailView(generic.DetailView):
#     model = Product
#     template_name = 'Site/ProductDetail.html'

#Create your views here.
def ProductDetailView(request,slug):
    ctx = {}
    product = Product.objects.get(slug = slug)
    ctx["product"] = product
    ctx["average_rating"] = product.average_rating
    ctx["recommended_products"] = recommended_products(user=request.user)[:10]
    ctx["store_products"] = Product.objects.filter(store = product.store)
    if not request.user.is_anonymous:
        ctx["purchased_product"] = request.user.profile.purchased_product(product)
        ctx["user_review"] = request.user.profile.get_review(product)
    try:
        current_order = request.user.profile.current_order
    except:
        current_order = None

    try:
        ctx["order_product"] = current_order.order_products.get(product=product)[:10]
    except Exception as e:
        print(e)
        ctx["order_product"] = None
    ctx["reviews"] = product.reviews.order_by("-created")
    if not request.user.is_anonymous:
        if request.method == 'POST':
            match request.POST.get('form_tag'):

                case "add_product":
                    current_order_expire_check(request.user)
                    current_order = request.user.profile.current_order
                    if current_order == None:
                        create_new_order(request.user)
                        current_order = request.user.profile.current_order
                    try:
                        current_order.update_product(product=product, quantity=request.POST.get('quantity'),
                                                     note=request.POST.get('quantity'))
                    except:
                        current_order.add_product(product=product,quantity=request.POST.get('quantity')
                                                  ,note=request.POST.get('note'))

                case "update_product":
                    current_order_expire_check(request.user)
                    current_order = request.user.profile.current_order

                    if current_order == None: raise ValidationError("Đơn hàng hiện tại đã hết hạn")
                    try:
                        current_order.update_product(product=product,quantity = request.POST.get('quantity'),
                                             note=request.POST.get('note'))
                    except:
                        current_order.add_product(product=product, quantity=request.POST.get('quantity')
                                                  , note=request.POST.get('note'))
                case "delete_product":
                    current_order_expire_check(request.user)
                    current_order = request.user.profile.current_order
                    if current_order == None: raise ValidationError("Đơn hàng hiện tại đã hết hạn")
                    current_order.delete_product(product)
                case "review_product":
                    product.make_review(request)
                    return render(request, 'Site/ProductDetail.html', ctx)

            return redirect('/product-list/1')
    return render(request, 'Site/ProductDetail.html',ctx)

def ProductListView(request,page_id=1):
    try:
        current_order_expire_check(request.user)
        current_order = request.user.profile.current_order
    except:
        current_order = None
    product = recommended_products(user=request.user)
    paginator = Paginator(product, 20)
    page = paginator.get_page(page_id)
    return ProductBaseView(request,paginator,page,{})

def ProductSearchView(request,search_keyword,page_id=1):
    ctx = {"search_keyword":search_keyword}
    try:
        current_order_expire_check(request.user)
        current_order = request.user.profile.current_order
    except:
        current_order = None
    product = searched_products(user=request.user,search_keyword=search_keyword)
    ctx["search_count"] = len(product)
    paginator = Paginator(product, 20)
    page = paginator.get_page(page_id)
    return ProductBaseView(request,paginator,page,ctx)


def ProductBaseView(request,paginator,page,ctx):
    ctx = ctx
    try:
        current_order_expire_check(request.user)
        current_order = request.user.profile.current_order
    except:
        current_order = None
    ctx["current_order"] = current_order


    ctx["page"] = page
    ctx["page_range"] = range(1,paginator.num_pages+1)

    if not request.user.is_anonymous:
        if request.method == "POST":
            match request.POST.get("form_tag"):
                case "create_order":
                    create_new_order(request.user)
            current_order = request.user.profile.current_order
            ctx["current_order"] = current_order
        if current_order != None: ctx["store_list"] = current_order.store_list
        else: ctx["store_list"] = None
    else:
        ctx["current_order"] = None
    return render(request,'Site/ProductList.html',ctx)
