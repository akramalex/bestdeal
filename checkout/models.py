import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    # Price-related fields
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    vat = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    VAT_PERCENTAGE = Decimal('20.0')  # 20% VAT rate

    def _generate_order_number(self):
        """ Generate a random, unique order number using UUID """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        ensuring VAT is applied **only** to VAT-applicable products.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or Decimal('0.00')

        # Calculate VAT **only** for products that require it
        vat_total = Decimal('0.00')
        for line_item in self.lineitems.all():
            if line_item.product.vat_applicable:  # ✅ Only apply VAT for VAT-applicable products
                vat_total += line_item.lineitem_total * self.VAT_PERCENTAGE / 100

        self.vat = vat_total  # ✅ Store VAT only for taxable products

        # Calculate delivery cost (only if order total is below free delivery threshold)
        if self.order_total > 0 and self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        else:
            self.delivery_cost = Decimal('0.00')

        # ✅ Grand total = Order Total + VAT (only for taxable products) + Delivery cost
        self.grand_total = self.order_total + self.vat + self.delivery_cost

        self.save()

    def save(self, *args, **kwargs):
        """ Override save method to set order number if not already set. """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)  # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()  # ✅ Update order total after saving

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
