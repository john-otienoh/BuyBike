"""Product Views"""

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, functions
from django.db.models.functions import Lower
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from reviews.forms import ReviewForm
# from reviews.models import Review
from .models import Product, Category
from .forms import ProductForm

# Create your views here.


def products(request):
    """All Product Views"""
    all_products = Product.objects.all()
    query, categories, sort, direction = None, None, None, None

    params = request.GET

    if request.GET:
        if "sort" in params:
            direction = params.get("direction", "asc")
            sort = params.get("sort", "name")
            if sort == "name":
                all_products = all_products.order_by(functions.Lower("name"))
            if sort == "category":
                sort = "category__slug"
            if "direction" in params:
                if direction == "desc":
                    sort = f"-{sort}"
            all_products = all_products.order_by(sort)

        if "category" in params:
            categories = params["category"].split(",")
            all_products = all_products.filter(category__slug__in=categories).distinct()
            current_categories = Category.objects.filter(slug__in=categories)
        else:
            current_categories = None

        if "q" in params:
            query = params["q"].strip()
            if query:
                all_products = all_products.filter(
                    Q(name__icontains=query)
                    | Q(description__icontains=query)
                    | Q(sku__icontains=query)
                ).distinct()
            else:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("products"))

    product_count = all_products.count()
    paginator = Paginator(all_products, 8)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    try:
        all_products = paginator.page(page_number)
    except EmptyPage:
        all_products = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        all_products = paginator.page(1)

    context = {
        "all_products": all_products,
        "search_query": query,
        "current_categories": categories,
        "current_sorting": f"{sort}_{direction}",
        "product_count": product_count,
        "page": page_obj,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product):
    product = get_object_or_404(Product, slug=product)
    return render(request, "products/product_detail.html", {"product": product})
