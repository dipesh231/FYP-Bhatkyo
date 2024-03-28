from django.urls import include, path
from . import views
from Accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.shopDashboard, name="shop"), 
    path('profile/', views.Sprofile, name='sprofile'),
]