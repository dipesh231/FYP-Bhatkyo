from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.nearby_shops, name='nearby_shops'),
    path('pinpoint_address/', views.pinpoint_address, name='pinpoint_address'),
    path('book/<int:shop_id>/', views.book_service, name='book_service'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('update-booking-status/', views.update_booking_status, name='update_booking_status'),
    path('rate_shop/<int:booking_id>/', views.rate_shop, name='rate_shop'),
    path('create_invoice/<int:booking_id>/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    
]
