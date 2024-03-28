from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerShop/', views.registerShop, name='registerShop'),

    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('shopDashboard/', views.shopDashboard, name='shopDashboard'),

    path('mechanicShop/', include('mechanic_shop.urls'))

]
