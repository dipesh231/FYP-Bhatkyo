from django.urls import path
from . import views

urlpatterns = [
    path('chatrooms/',views.room, name='rooms'),
    path('<slug:slug>/', views.chatroom, name='chatroom')

]