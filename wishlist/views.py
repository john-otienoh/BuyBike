from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wishlist
from products.models import Product
from django.http import JsonResponse

# Create your views here.
class WishlistView(LoginRequiredMixin, View):
    def get(self, request):
        wishlist, _  = Wishlist.objects.get_or_create(user=request.user)
        products = wishlist.products.filter(is_available=True).prefetch_related('images')
        return render(request, 'wishlist/wishlist.html', {'products': products})

class ToggleWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        wishlist, _ = Wishlist.objects.get_or_create(user.request.user)
        if wishlist.products.filter(pk=product_id).exists():
            wishlist.products.remove(product)
            in_wishlist = False
            msg = "Removed from wishlist."
        else:
            wishlist.products.add(product)
            in_wishlist = True
            msg = "Added to wishlist."
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {
                    'in_wishlist': in_wishlist, 
                    'message': msg,
                    'wishlist_count':wishlist.products.count()
                }
            )
        messages.success(request, msg)
        return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist'))