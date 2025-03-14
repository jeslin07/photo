from django.contrib import admin
from .models import ContactMessage
from .models import SaveTheDate 
from .models import Product
# Register your models here.


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    actions = ['mark_as_read', 'mark_as_unread']

admin.site.register(ContactMessage, ContactMessageAdmin)



@admin.register(SaveTheDate)
class SaveTheDateAdmin(admin.ModelAdmin):
    list_display = ('couples_names', 'email', 'wedding_date', 'is_contacted')
    search_fields = ('couples_names', 'email')
    list_filter = ('wedding_date', 'is_contacted')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_url') 