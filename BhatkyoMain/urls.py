from django.urls import include, path
from BhatkyoMain import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.show_products, name='show_products'),

 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

