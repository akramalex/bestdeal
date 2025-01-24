from django.contrib import admin
from .models import Product, Category, DiscountTier

# Inline model for DiscountTier
class DiscountTierInline(admin.TabularInline):
    model = DiscountTier  # Reference the DiscountTier model
    extra = 1  # Show one empty row by default for adding new tiers
    fields = ('quantity', 'price')  # Display these fields in the inline form

# ProductAdmin with DiscountTier Inline
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'vat_applicable')  # Columns in the list view
    fields = ('name', 'price', 'category', 'image', 'vat_applicable', 'description')  # Fields in the product form
    inlines = [DiscountTierInline]  # Add DiscountTier inline editing

# CategoryAdmin for Category management
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')  # Columns in the list view

# Register models with the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
