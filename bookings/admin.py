from django.contrib import admin

from bookings.models import BookService, Invoice, InvoiceProduct, RateBooking

# Register your models here.

class serviceAdmin(admin.ModelAdmin):
    list_display = ('')
class BookServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop', 'services', 'status', 'location', 'date')
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

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('booking', 'service_hours', 'total_amount', 'created_at')
    inlines = [InvoiceProductInline]

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceProduct)
