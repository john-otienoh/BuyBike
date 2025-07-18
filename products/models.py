from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    """Category Model"""

    name = models.CharField(max_length=256, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    slug = models.SlugField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        """get_friendly_name function"""
        return self.friendly_name

    def save(self, *args, **kwargs):
        """Prepopulate slug field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("product_by_category", args=[self.slug])

    class Meta:
        """Category Model Meta"""

        verbose_name_plural = "Categories"
        ordering = ["name"]


class Product(models.Model):
    """[product model]"""

    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    slug = models.SlugField(
        max_length=250,
        unique=True,
    )
    specs = models.JSONField(default=dict)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="shop/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Product model ordering"""

        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Prepopulate slug field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("product_detail", args=[self.slug])
