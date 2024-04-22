from django.contrib import admin

from .models import Product, ProductPayment, PurchasedProduct

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'total_quantity','availability','price','created_at')
    list_display_links = ('user', 'product_name')

admin.site.register(Product, ProductAdmin)

class PurchasedProductInline(admin.TabularInline):
    model = PurchasedProduct
    extra = 0

@admin.register(ProductPayment)
class ProductPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date')
    inlines = [PurchasedProductInline]

@admin.register(PurchasedProduct)
class PurchasedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'payment', 'shop', 'quantity')