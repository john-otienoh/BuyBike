from django.urls import path 
from . import views 

app_name = 'wishlist' 

urlpatterns = [
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.ToggleWishlistView.as_view(), name='toggle_wishlist'),    
]