"""Product Urls"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name="products"),
    path("<slug:product>/", views.product_detail, name="product_detail"),
]
