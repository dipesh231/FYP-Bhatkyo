from django.contrib import admin
from bookings.models import BookService, Invoice, InvoiceProduct, InvoiceService, RateBooking

# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('')  # Add appropriate fields here

class BookServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop', 'status', 'location', 'date')
    list_filter = ('status', 'date')
    search_fields = ('user__email', 'shop__name', 'services__name', 'location')

admin.site.register(BookService, BookServiceAdmin)

class RateBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_service', 'review')
    search_fields = ('user__email', 'book_service__problem_description', 'review')

admin.site.register(RateBooking, RateBookingAdmin)

class InvoiceProductInline(admin.TabularInline):
    model = InvoiceProduct
    extra = 0

class InvoiceServiceInline(admin.TabularInline):
    model = InvoiceService
    extra = 0

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('booking', 'total_amount', 'created_at')
    inlines = [InvoiceProductInline, InvoiceServiceInline]

admin.site.register(Invoice, InvoiceAdmin)

class InvoiceProductAdmin(admin.ModelAdmin):  # Added admin configuration for InvoiceProduct
    list_display = ('invoice', 'product', 'quantity')

admin.site.register(InvoiceProduct, InvoiceProductAdmin)

class InvoiceServiceAdmin(admin.ModelAdmin):  # Added admin configuration for InvoiceService
    list_display = ('invoice', 'service', 'hours')

admin.site.register(InvoiceService, InvoiceServiceAdmin)
