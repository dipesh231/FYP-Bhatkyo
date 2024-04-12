from django.urls import include, path
from . import views
from Accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.shopDashboard, name="shop"), 
    path('profile/', views.Sprofile, name='sprofile'),
    path('bookings/', views.Bookings, name='bookings'),
    path('add_product/',views.add_product, name='add_product'),
    path('products/', views.Products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),

    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('booking_details/<int:booking_id>/', views.booking_details, name='booking_details'),
    
]