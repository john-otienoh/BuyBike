"""Product Urls"""

from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/category/<slug:slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.ProductListView.as_view(), name='search'),
    path('products/<slug:slug>/review/', views.AddReviewView.as_view(), name='add_review'),
]
