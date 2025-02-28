from django.contrib import admin
from .models import ContactMessage


# Customize the admin interface for ContactMessage
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject',  'is_read',  'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_editable = ('is_read',)

# Register the ContactMessage model with the admin panel


admin.site.register(ContactMessage, ContactMessageAdmin)
