from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerShop/', views.registerShop, name='registerShop'),

    path('login/', views.custom_login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('shopDashboard/', views.shopDashboard, name='shopDashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name = 'activate'),
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name = 'reset_password_validate'),
    path('reset_password/', views.reset_password, name = 'reset_password'),


    path('mechanicShop/', include('mechanic_shop.urls')),
    path('customer/', include('customer.urls')),

]
