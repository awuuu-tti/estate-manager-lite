from django.contrib import admin
from .models import Property, ViewingRequest


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'deal_type', 'price', 'address', 'status', 'created_at')
    list_filter = ('deal_type', 'status')
    search_fields = ('title', 'address', 'description')


@admin.register(ViewingRequest)
class ViewingRequestAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'property', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('client_name', 'phone', 'property__title')
    readonly_fields = ('created_at',)
