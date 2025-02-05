from django.db import models
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
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    quantity = models.PositiveIntegerField()  # Quantity for the discount
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Discounted price for this quantity

    def __str__(self):
        return f"{self.quantity}+ units: ${self.price}"
