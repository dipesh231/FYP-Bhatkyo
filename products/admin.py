from django.contrib import admin

from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'total_quantity','availability','price','created_at')
    list_display_links = ('user', 'product_name')

admin.site.register(Product, ProductAdmin)