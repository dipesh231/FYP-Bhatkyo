from django.urls import path
from BhatkyoMain import views

urlpatterns = [
    path('',views.index, name='index')
]