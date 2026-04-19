from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q, Avg, Count
from django.utils import timezone
from django.conf import settings
from .context_processors import get_or_create_cart
from products.models import Product
from .models import CartItem, Cart

class CartView(View):
    def get(self):
        cart = get_or_create_cart(request)
        items = cart.items.select_related(
            'product', 'variant'
        ).prefetch_related('product__images')

        coupon_code = self.request.session.get('coupon_code')
        discount = 0
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid:
                    if coupon.discount_type == 'percentage':
                        discount = cart.subtotal * coupon.discount_value / 100
                    elif coupon.discount_type == 'fixed':
                        discount = coupon.discount_value
                else:
                    del request.session['coupon_code']
                    coupon = None
            except Coupon.DoesNotExist:
                del request.session['coupon_code']
        return render(request, 'store/cart.html', {
            'cart': cart,
            'items': items,
            'coupon': coupon,
            'discount': discount,
            'total_after_discount': max(cart.subtotal - discount, 0),
        })

class AddToCartView(View):
    def post(self, request, product_id):
        product= get_object_or_404(
            Product, pk=product_id, is_available=True
        )
        quantity = int(request.POST.get('quantity', 1))
        variant_id = request.POST.get('variant_id')
        variant = None

        if quantity < 1:
            quantity = 1
        
        if product.stock < quantity:
            messages.error(request, f"Only {product.stock} units available.")
            return redirect(product.get_absolute_url())
        
        cart = get_or_create_cart(request)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, variant=variant, defaults={'quantity': quantity}
        )
        if not created:
            item.quantity = min(item.quantity + quantity, product.stock)
            item.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {
                    'success': True, 
                    'cart_count': cart.total_items,
                    'message': f'"{product.name}" added to cart.'
                }
            )
        messages.success(request, f'"{product.name}" added to your cart.')
        return redirect('cart:cart')

class UpdateCartView(View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, pk=item_id)
        cart = get_or_create_cart(request)

        if item.cart != cart:
            return JsonResponse(
                {'error': 'Forbidden'}, status=403
            )
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            item.delete()
        else:
            item.quantity = min(quantity, item.product.stock)
            item.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': cart.total_items,
                'line_total': str(item.line_total if quantity >= 1 else 0),
                'subtotal': str(cart.subtotal),
            })
        return redirect('cart:cart')
class ApplyCouponView(View):
    def post(self, request):
        code = request.POST.get('coupon_code', '').strip().upper()
        cart = get_or_create_cart(request)

        try:
            coupon = Coupon.objects.get(code=code)

            if not coupon.is_valid:
                messages.error(request, "This coupon is expired or no longer valid.")
            elif cart.subtotal < coupon.min_order_value:
                messages.error(request, f"Minimum order of ${coupon.min_order_value} required.")
            else:
                request.session['coupon_code'] = code
                messages.success(request, f'Coupon "{code}" applied!')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid Coupon Code')
        return redirect('cart:cart')
    