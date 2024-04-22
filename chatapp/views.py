from django.shortcuts import get_object_or_404, render
from Accounts.models import User
from mechanic_shop.models import Shop
from bookings.models import BookService
from chatapp.models import ChatMessage, ChatRoom
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def room(request):
    if request.user.role == User.MECHANIC_SHOP:
        # If the user has a shop associated with their profile, get the shop's name
        shop = get_object_or_404(Shop, user=request.user)
        shop_name = shop.shop_name
        # Filter chatrooms where the shop's name is present
        chatrooms = ChatRoom.objects.filter(name__icontains=shop_name)
    else:
        # If the user is not a shop owner, show chatrooms where their username is present
        username = request.user.username
        chatrooms = ChatRoom.objects.filter(name__icontains=username)
    return render(request, 'chatapp/index.html', {'chatrooms': chatrooms})

def chatroom(request,slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    messages = ChatMessage.objects.filter(room = chatroom)[0:30]
    return render(request, 'chatapp/room.html', {'chatroom':chatroom, 'messages':messages})



@receiver(post_save, sender=BookService)
def create_chat_room_for_booking(sender, instance, created, **kwargs):
    if created:
        shop_name = instance.shop.shop_name if instance.shop else "Unknown Shop"
        chat_room_name = f"Chat with {instance.user.username} and {shop_name}"
        base_slug = slugify(chat_room_name)
        try:
            existing_chat_room = ChatRoom.objects.get(name=chat_room_name)
        except ChatRoom.DoesNotExist:
            ChatRoom.objects.create(name=chat_room_name, slug=base_slug)

from django.http import JsonResponse
from django.core.serializers import serialize

def get_chat_messages(request):
    # Fetch chat messages from the database
    messages = ChatMessage.objects.all()
    # Serialize the messages to JSON
    serialized_messages = serialize('json', messages, fields=('user', 'room', 'message_content', 'date'))
    # Return the serialized messages as JSON response
    return JsonResponse({'messages': serialized_messages})