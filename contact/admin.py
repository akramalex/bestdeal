from django.contrib import admin
from .models import ContactMessage

# Customize the admin interface for ContactMessage
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject',  'is_read',  'created_at')  # Fields displayed in the admin list view
    search_fields = ('name', 'email', 'subject')  # Searchable fields in the admin panel
    list_filter = ('created_at',)  # Filter options in the admin panel
    ordering = ('-created_at',)  # Order by creation date descending
    list_editable = ('is_read',)

# Register the ContactMessage model with the admin panel
admin.site.register(ContactMessage, ContactMessageAdmin)
