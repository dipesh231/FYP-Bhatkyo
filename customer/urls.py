from django.urls import include, path
from . import views
from Accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.customerDashboard, name = 'customer'),
    path('profile/', views.Cprofile, name='cprofile'),
    path('myBookings/', views.myBookings, name='myBookings'),
    path('my_booking_details/<int:booking_id>/', views.my_booking_details, name='my_booking_details'),
    path('my_invoice/<int:invoice_id>/', views.view_invoice_detail, name='view_invoice_detail'),
    path('my_invoice/<int:invoice_id>/mark-as-paid/', views.mark_as_paid, name='mark_as_paid'),



]    
