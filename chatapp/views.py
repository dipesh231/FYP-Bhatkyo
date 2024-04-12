from django.shortcuts import render
from bookings.models import BookService
from chatapp.models import ChatMessage, ChatRoom
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your views here.
def room(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chatapp/index.html', {'chatrooms':chatrooms})

def chatroom(request,slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    messages = ChatMessage.objects.filter(room = chatroom)[0:30]
    return render(request, 'chatapp/room.html', {'chatroom':chatroom, 'messages':messages})


@receiver(post_save, sender=BookService)
def create_chat_room(sender, instance, created, **kwargs):
    if created:
        # Access the associated shop through the ForeignKey relationship
        shop_name = instance.shop.shop_name if instance.shop else "Unknown Shop"
        # Define the name for the ChatRoom
        chat_room_name = f"ChatRoom for {instance.user.username} and {shop_name}"
        # Create a slug based on the name or any other unique identifier
        base_slug = f"{instance.user.username}-{shop_name}".lower().replace(" ", "-")
        # Check if a ChatRoom with the same user and shop already exists
        try:
            existing_chat_room = ChatRoom.objects.get(name=chat_room_name)
        except ChatRoom.DoesNotExist:
            # Create the ChatRoom instance
            ChatRoom.objects.create(name=chat_room_name, slug=base_slug)


