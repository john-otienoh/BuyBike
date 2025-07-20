"""Admin products"""

from django.contrib import admin
from .models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""

    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""

    list_display = [
        "name",
        "sku",
        "rating",
        "is_available",
        "category",
        "price",
        "stock",
    ]
    list_filter = ["is_available", "category"]
    search_fields = ["name", "sku"]
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ["category"]
    date_hierarchy = "updated_at"
    ordering = ["updated_at", "price"]
    show_facets = admin.ShowFacets.ALWAYS
