from django.urls import include, path
from . import views
from Accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.shopDashboard, name="shop"), 
    path('profile/', views.Sprofile, name='sprofile'),
    path('bookings/', views.Bookings, name='bookings'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('booking_details/<int:booking_id>/', views.booking_details, name='booking_details'),
    
]