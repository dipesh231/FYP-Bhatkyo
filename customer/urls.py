from django.urls import include, path
from . import views
from Accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.customerDashboard, name = 'customer'),
    path('profile/', views.Cprofile, name='cprofile'),
    path('myBookings/', views.myBookings, name='myBookings'),


]    
