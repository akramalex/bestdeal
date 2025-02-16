from django.contrib import admin
from .models import Product, Category, DiscountTier, Review

# Inline model for DiscountTier
class DiscountTierInline(admin.TabularInline):
    model = DiscountTier
    extra = 1
    fields = ('quantity', 'price')

# ProductAdmin with DiscountTier Inline
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price', 'category', 'rating', 'image', 'has_sizes', 'vat_applicable')
    fields = ('name', 'price', 'category', 'image', 'vat_applicable', 'has_sizes', 'description')
    inlines = [DiscountTierInline]
    ordering = ('sku',)

# CategoryAdmin for Category management
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')

# ReviewAdmin for managing reviews
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')  # Show these fields in the list view
    search_fields = ('user__username', 'product__name', 'comment')  # Enable search by username, product name, and comment
    list_filter = ('rating', 'created_at')  # Add filters for easier navigation
    ordering = ('-created_at',)  # Show newest reviews first

# Register models with the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
