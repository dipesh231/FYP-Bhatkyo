from django.shortcuts import get_object_or_404, render, redirect
from .models import RateBooking, Shop, BookService
from .forms import BookServiceForm
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
# from django.contrib.gis.geos import Point
from django.shortcuts import render
from .models import Shop, Service

def search_shops(request):
    if request.method == 'POST':
        user_location = request.POST.get('location')
        user_latitude, user_longitude = get_coordinates_from_address(user_location)

        distance = float(request.POST.get('distance'))
        selected_services = request.POST.getlist('services')

        user_location_point = Point(user_longitude, user_latitude, srid=4326)

        nearby_shops = Shop.objects.filter(
            user_profile__latitude__isnull=False,
            user_profile__longitude__isnull=False
        ).annotate(
            distance=Distance('user_profile__location', user_location_point)
        ).filter(
            distance__lte=distance,
            services__in=selected_services
        ).distinct()

        return render(request, 'bookings/search_results.html', {'nearby_shops': nearby_shops})
    else:
        # Render the search form with available services
        services = Service.objects.all()
        return render(request, 'bookings/search_form.html', {'services': services})

def get_coordinates_from_address(address):
    # This function should use geocoding APIs (like Google Maps Geocoding API or Nominatim)
    # to get latitude and longitude from the address provided by the user.
    # For simplicity, I'm assuming it's already implemented.
    latitude = 28.3949
    longitude = 84.124
    return latitude, longitude


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
        feedback = request.POST.get('feedback')
        booking = get_object_or_404(BookService, pk=booking_id)
        booking.status = status
        booking.feedback = feedback
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



