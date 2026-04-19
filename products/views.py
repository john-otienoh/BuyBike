"""Product Views"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q, Avg, Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Brand, Category, Product
from .forms import ProductSearchForm
# Create your views here.

class ProductListView(View):
    template_name = 'products/product_list.html'
    paginate_by = getattr(settings, 'PRODUCTS_PER_PAGE', 12)
    
    def get(self, request, slug=None):
        products = Product.objects.filter(is_available=True).select_related(
            'category', 'brand'
        ).prefetch_related('images', 'reviews')
        category = None

        if slug:
            category = get_object_or_404(Category, slug=slug, is_active=True)
            sub_categories = category.children.values_list('id', flat=True)
            products = products.filter(
                Q(category=category) | Q(category__in=sub_categories)
            )
        
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            brand_slug = form.cleaned_data.get('brand')
            bike_type = form.cleaned_data.get('bike_type')
            sort = form.cleaned_data.get('sort')

            if q:
                products = products.filter(
                    Q(name__icontains=q) | Q(description__icontains=q) | Q(brand__name__icontains=q) | Q(category__name__icontains=q)
                )
            
            if min_price:
                products = products.filter(price__gte=min_price)
            if max_price:
                products = products.filter(price__lte=max_price)
            if brand_slug:
                products = products.filter(brand__slug=brand_slug)
            if bike_type:
                products = products.filter(bike_type=bike_type)
            
            if sort == 'price_asc':
                products = products.order_by('price')
            elif sort == 'price-desc':
                products = products.order_by('-price')
            elif sort == 'newest':
                products = products.order_by('-created_at')
            elif sort == 'rating':
                products = products.annotate(
                    avg_r=Avg('reviews__rating')
                ).order_by('-avg_r')
            elif sort == 'popular':
                products = products.order_by('-views_count')
        
        paginator = Paginator(products, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        all_brands = Brand.objects.filter(is_active=True)
        bike_type_choices = Product.BIKE_TYPE_CHOICES

        return render(request, self.template_name, {
            'products': page_obj,
            'category': category,
            'form': form,
            'all_brands': all_brands,
            'bike_type_choices': bike_type_choices,
            'total_count': paginator.count,
        })

class ProductDetailView(View):
    template_name = 'products/product_detail.html'

    def get(self, request, slug):
        product = get_object_or_404(
            Product.objects.select_related('category', 'brand')
                           .prefetch_related('images', 'variants', 'reviews__user'),
            slug=slug, is_available=True
        )
        # Increment view count
        Product.objects.filter(pk=product.pk).update(views_count=product.views_count + 1)

        related = Product.objects.filter(
            category=product.category, is_available=True
        ).exclude(pk=product.pk).prefetch_related('images')[:4]

        reviews = product.reviews.filter(is_approved=True).select_related('user')
        review_form = ReviewForm()

        user_review = None
        if request.user.is_authenticated:
            user_review = Review.objects.filter(product=product, user=request.user).first()

        in_wishlist = False
        if request.user.is_authenticated:
            try:
                in_wishlist = Wishlist.objects.get(user=request.user).products.filter(pk=product.pk).exists()
            except Wishlist.DoesNotExist:
                pass

        return render(request, self.template_name, {
            'product': product,
            'related_products': related,
            'reviews': reviews,
            'review_form': review_form,
            'user_review': user_review,
            'in_wishlist': in_wishlist,
        })

class AddReviweView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if Review.objects.filter(product=product, user=request.user).exists():
            messages.warning(request, "You've already reviewed this product")
            return redirect(product.get_absolute_url())
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user

            review.is_verified_purchase = Order.objects.filter(
                user=request.user, items__product=product, payment_status=paid
            ).exists()

            review.save()
            messages.success(request, "Review submitted. It will appear after approval.")
        else:
            messages.error(request, "Invalid review. Please check the form.")
        return redirect(product.get_absolute_url())