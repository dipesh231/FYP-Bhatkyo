from django.urls import path
from . import views
from .views import search_shops

urlpatterns = [
    path('search/', views.search_shops, name='search_shops'),
    path('book/<int:shop_id>/', views.book_service, name='book_service'),
    path('update-booking-status/', views.update_booking_status, name='update_booking_status'),
    path('rate_shop/<int:booking_id>/', views.rate_shop, name='rate_shop'),
    


]
