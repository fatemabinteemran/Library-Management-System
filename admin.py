#myapp_admin
from django.contrib import admin
from .models import Product,Category,Event,ContactMessage,BlogPost
from django.conf import settings
from django.urls import path

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email')
    actions = ['send_response']

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(BlogPost)