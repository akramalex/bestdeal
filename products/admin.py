from django.contrib import admin
from .models import Product, Category, Review


# ProductAdmin (Removed DiscountTier Inline)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku', 'name', 'price', 'category', 'rating', 'image',
        'has_sizes', 'vat_applicable'
    )  # Split into multiple lines
    fields = (
        'name', 'price', 'category', 'image', 'vat_applicable',
        'has_sizes', 'description'
    )  # Split into multiple lines
    ordering = ('sku',)


# CategoryAdmin for Category management
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')


# ReviewAdmin for managing reviews
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

# Register models with the admin site


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
