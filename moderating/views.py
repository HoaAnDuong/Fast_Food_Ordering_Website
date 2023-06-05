from django.shortcuts import render
from products.models import *
from django.http import HttpResponse,Http404
import json
from django.core.paginator import Paginator
from django.db.models import Count, F, Value, Q, Avg
from .utils import *
# Create your views here.

def ModeratorView(request):
    ctx = {}
    ctx["product_status"] = Product_Status.objects.all()
    return render(request,"Site/Moderator.html",ctx)

def GetModeratedProduct(request,page_id):
    ctx = {}
    if request.method == "POST":
        if request.user.profile.is_moderator:
            print(request.POST)
            products = Product.objects.all()
            product_name = request.POST.get('product_name')
            status = request.POST.get('status')

            if product_name:
                keyword_list = product_name.split()
                if len(keyword_list) == 0: keyword_list = [""]
                search_query = Q(name__contains=keyword_list[0])
                for i in range(1, len(keyword_list)):
                    search_query = search_query & Q(name__contains=keyword_list[i])
                products = products.filter(search_query)

            if status and status != "":
                products = products.filter(status__code = status)

            paginator = Paginator(products,10)
            page = paginator.get_page(page_id)

            ctx["page_id"] = page.number
            ctx["num_pages"] = paginator.num_pages
            ctx["products"] = [
                {
                    "name":product.name,
                    "url":f"/moderator/products/{product.slug}",
                    "image_url":product.image.url,
                    "category":product.category.name,
                    "status":product.status.code,
                    "price":product.price.__str__(),
                    "rating":product.average_rating,
                }
                for product in page
            ]
            return HttpResponse(json.dumps(ctx), status=200)
    else:
        return Http404()

def ModeratedProductView(request,slug):
    if request.user.profile.is_moderator:
        ctx = {}
        product = Product.objects.get(slug = slug)
        ctx["product"] = product
        categories = Category.objects.all()
        ctx["categories"] = categories

        reviews = Product_Review.objects.filter(product__slug = slug)
        paginator = Paginator(reviews, 10)
        ctx["page_range"] = range(1, paginator.num_pages + 1) if len(reviews) != 0 else None

        if request.method == "POST":
            match request.POST.get('form_tag'):
                case "ban_product":
                    ban_product(request,product)
                case "unban_product":
                    unban_product(request, product)
                case "verify_product":
                    verify_product(request, product)

    return render(request,"Site/ModeratedProduct.html",ctx)

def GetProductReviews(request,slug,page_id):
    ctx = {}
    if request.method == "POST":
        if request.user.profile.is_moderator:
            reviews = Product_Review.objects.filter(product__slug = slug)

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
            filtered_rating = float(request.POST.get('filtered_rating')) if request.POST.get('filtered_rating') else None

            if filtered_name:
                word_list = filtered_name.split()
                if len(word_list) == 0: word_list = [""]
                search_query = (Q(author__profile__first_name__contains=word_list[0])|Q(author__profile__last_name__contains=word_list[0]))
                for i in range(1, len(word_list)):
                    search_query = search_query & (Q(author__profile__first_name__contains=word_list[i])|Q(author__profile__last_name__contains=word_list[i]))
                reviews = reviews.filter(search_query)

            if filtered_rating:
                reviews = reviews.filter(rating = filtered_rating)

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
                    "id":review.id,
                }
                for review in page
            ]
        return HttpResponse(json.dumps(ctx), status=200)
    else:
        return Http404()
