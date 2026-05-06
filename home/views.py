"""Home Views"""
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q, Avg
from products.models import Brand, Category, Product
from promotions.models import Banner
from newsletter.forms import NewsletterForm

# Create your views here.
class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        featured = Product.objects.filter(is_available=True, is_featured=True).select_related(
            'category', 'brand').prefetch_related('images')[:8]
        new_arrivals = Product.objects.filter(is_available=True, is_new_arrival=True).select_related(
            'category', 'brand').prefetch_related('images')[:8]
        top_rated = Product.objects.filter(is_available=True).annotate(
            avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True))
        ).order_by('-avg_rating').select_related('category', 'brand').prefetch_related('images')[:6]
        categories = Category.objects.filter(is_active=True, parent=None)[:6]
        banners = Banner.objects.filter(is_active=True)[:5]
        brands = Brand.objects.filter(is_active=True)[:8]
        newsletter_form = NewsletterForm()
        return render(request, self.template_name, {
            'featured_products': featured,
            'new_arrivals': new_arrivals,
            'top_rated': top_rated,
            'categories': categories,
            'banners': banners,
            'brands': brands,
            'newsletter_form': newsletter_form,
        })

class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["stats"] = [
            {"value": "200k", "label": "Customers"},
            {"value": "50+", "label": "Countries"},
            {"value": "15", "label": "Years"},
            {"value": "4.9★", "label": "Avg. Rating"},
        ]
        return context

class ContactView(TemplateView):
    template_name = 'home/contact.html'
