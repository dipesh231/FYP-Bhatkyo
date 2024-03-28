from django.contrib import admin

from bookings.models import BookService, RateBooking

# Register your models here.

class serviceAdmin(admin.ModelAdmin):
    list_display = ('')
admin.site.register(BookService)
admin.site.register(RateBooking)