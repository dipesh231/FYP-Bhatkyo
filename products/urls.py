from django.urls import path
from . import views
urlpatterns = [
    path('products/', views.show_products, name='show_products'),

    path('product/<int:id>/', views.productDetail, name='productDetail'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
    views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
    views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('khalti-init',views.initkhalti,name='init'),
    path('verify', views.verifyKhalti, name='verify')
]
