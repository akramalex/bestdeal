from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    vat_applicable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def price_with_vat(self):
        """
        Returns the price including VAT if applicable.
        """
        if self.vat_applicable:
            return self.price * Decimal('1.20')  # Adds 20% to the price
        return self.price

    def get_price_for_quantity(self, quantity):
        """
        Returns the discounted price based on the quantity.
        """
        discount_tiers = self.discounttier_set.all().order_by('quantity')
        for tier in discount_tiers:
            if quantity >= tier.quantity:
                return tier.price
        return self.price  # Return default price if no tier matches


class DiscountTier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}+ units: ${self.price}"


class Review(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=5
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"Review by {self.user.username} - {self.product.name}"


def update_product_rating(product):
    """
    Recalculates and updates the product's rating based on all reviews.
    """
    print(f"🔄 Updating rating for product: {product.name}")  # Debugging

    reviews = product.reviews.all()
    if reviews.exists():
        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        product.rating = round(avg_rating, 2)  # Keep two decimal places
        print(f"✅ New calculated rating: {product.rating}")  # Debugging
    else:
        product.rating = None  # Reset rating if no reviews exist
        print("❌ No reviews found. Resetting rating.")  # Debugging

    product.save()
    print("✅ Product rating updated in database.")  # Debugging

    """
    Recalculates and updates the product's rating based on all reviews.
    """
    reviews = product.reviews.all()
    if reviews.exists():
        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        product.rating = round(avg_rating, 2)  # Keep two decimal places
    else:
        product.rating = None  # Reset rating if no reviews exist
    product.save()
