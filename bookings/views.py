# model.py

from django.shortcuts import get_object_or_404, render, redirect
from .models import RateBooking, Shop, BookService
from .forms import BookServiceForm

# model.py

from django.shortcuts import render, redirect
from .models import Shop, BookService
from .forms import BookServiceForm

def book_service(request, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    user_id = request.user.id  # Assuming user is authenticated
    if request.method == 'POST':
        form = BookServiceForm(shop=shop, data=request.POST)
        if form.is_valid():
            book_service = form.save(commit=False)
            book_service.user_id = user_id
            book_service.shop = shop
            book_service.save()
            return redirect('index')
    else:
        form = BookServiceForm(shop=shop)
    return render(request, 'bookings/book_service.html', {'shop': shop, 'form': form})

def update_booking_status(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        status = request.POST.get('status')
        booking = get_object_or_404(BookService, pk=booking_id)
        booking.status = status
        booking.save()
        return redirect('shopDashboard')
    
def rate_shop(request, booking_id):
    booking = get_object_or_404(BookService, pk=booking_id)
    if request.method == 'POST':
      
        user = request.user
        review_text = request.POST.get('review')
        RateBooking.objects.create(user=user, book_service=booking, review=review_text)
        return redirect('customerDashboard')  # Redirect to some page after submission
    else:
        
        pass
    context = {
        'booking':booking
    }
    return render(request, 'bookings/rate_booking.html', context)



