from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product
# Create your views here.

def cart(request):
    """Render the Cart Contents"""
    return render(request, 'cart/cart.html')

def add_to_cart(request, id):
    """Add a quantity of product to cart"""
    product = get_object_or_404(Product, pk=id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('bag', {})
    if id in list(cart.keys()):
        cart[id] += quantity
        messages.success(
            request,(
                f'Updated {product.name} quantity to '
                f'{cart[id]}'
            )
        )
    else:
        cart[id] = quantity
        messages.success(request, f'Added {product.name} to your cart')
    request.session['cart'] = cart
    return redirect(redirect_url)
