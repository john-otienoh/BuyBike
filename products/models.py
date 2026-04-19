from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

import uuid


# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
class Category(models.Model):
    """Category Model"""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=256, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Category Model Meta"""

        verbose_name_plural = "Categories"
        verbose_name = "category"
        indexes = [
            models.Index(fields=["name"]),
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Prepopulate slug field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """[product model]"""

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]
    BIKE_TYPE_CHOICES = [
        ('mountain', 'Mountain Bike'),
        ('road', 'Road Bike'),
        ('hybrid', 'Hybrid Bike'),
        ('electric', 'Electric Bike'),
        ('bmx', 'BMX'),
        ('gravel', 'Gravel Bike'),
        ('kids', 'Kids Bike'),
        ('cruiser', 'Cruiser'),
        ('folding', 'Folding Bike'),
        ('accessories', 'Accessories & Parts'),
        ('clothing', 'Clothing & Gear'),
        ('other', 'Other'),
    ]

    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='products'
    )
    sku = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=256)
    bike_type = models.CharField(max_length=20, choices=BIKE_TYPE_CHOICES, default='other')
    condition = models.CharField(max_length=15, choices=CONDITION_CHOICES, default='new')
    short_description = models.CharField(max_length=500, blank=True)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
        help_text='Original/crossed-out price for sale display')
    specifications = models.JSONField(default=dict, blank=True,
        help_text='JSON field: {"Frame": "Aluminum", "Gears": "21-speed", ...}')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True
    )
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='kg')
    frame_size = models.CharField(max_length=50, blank=True, help_text='e.g. S/M/L or 26"/29"')
    wheel_size = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=100, blank=True)

    thumbnail = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Product model ordering"""

        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=['is_available', 'is_featured']),
            models.Index(fields=['category', 'is_available']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Prepopulate slug field"""
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = str(uuid.uuid4()).upper()[:10]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return Absolute url"""
        return reverse("product:product_detail", args=[self.slug])

    @property
    def is_in_stock(self):
        return self.stock > 0
    
    @property
    def is_low_stock(self):
        return 0 < self.stock <= self.low_stock_threshold
    
    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int(
                (
                    (self.compare_price - self.price) / self.compare_price
                ) * 100
            )
        return 0
    
    @property
    def average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0
    
    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()
    
    @property
    def primary_image(self):
        self.images.filter(is_primary=True).first()
        return img or self.images.first()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self) -> str:
        return f"{self.product.name} - Image {self.id}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product, is_primary=True
            ).update(is_primary=False)
        super().save(*args, **kwargs)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100, help_text='e.g. "Red / Large"')
    sku_suffix = models.CharField(max_length=20, blank=True)
    price_modifier = models.DecimalField(max_digits=8, decimal_places=2, default=0,
        help_text='Added to base price (can be negative)')
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def final_price(self):
        return self.product.price + self.price_modifier
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_verified_purchase = models.BooleanField(default=False)
    helpful_votes = models.PositiveIntegerField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering= ['-created_at']
    
    def __str__(self) -> str:
        return f"{self.user.username} → {self.product.name} ({self.rating}★)"