from django.contrib import admin


from mechanic_shop.models import Service, Shop

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'shop_name')

admin.site.register(Shop, ShopAdmin)
admin.site.register(Service)
