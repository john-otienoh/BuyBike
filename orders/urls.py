from django.urls import path 
from . import views 

app_name = 'orders' 

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/<str:order_number>/', views.OrderSuccessView.as_view(), name='order_success'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<str:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),
]