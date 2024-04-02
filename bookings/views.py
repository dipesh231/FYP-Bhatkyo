from decimal import Decimal
import math
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from products.models import Product
from .models import Invoice, InvoiceProduct, RateBooking, BookService
from .forms import BookServiceForm
from django.shortcuts import render
from mechanic_shop.models import Service, Shop
from django.db.models import F
from django.contrib import messages



def pinpoint_address(request):
    services = Service.objects.all()
    return render(request, 'bookings/search_form.html', {'services': services})

def nearby_shops(request):
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        selected_service_id = request.POST.get('service')
        
        # Store selected service ID in session
        request.session['selected_service_id'] = selected_service_id
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        # Print message if selected_service_id is saved in session
        if selected_service_id:
            print("Selected service ID saved in session:", selected_service_id)
        # Print latitude and longitude saved in session
        print("Latitude saved in session:", latitude)
        print("Longitude saved in session:", longitude)
        
        # Convert 10 kilometers to degrees (approximate conversion)
        range_distance_km = 5
        latitude_range = range_distance_km / 111
        longitude_range = range_distance_km / (111 * abs(math.cos(math.radians(latitude))))
        
        # Calculate latitude and longitude ranges
        latitude_min = latitude - latitude_range
        latitude_max = latitude + latitude_range
        longitude_min = longitude - longitude_range
        longitude_max = longitude + longitude_range
        
        # Query nearby shops based on latitude, longitude, and selected service
        nearby_shops = Shop.objects.filter(
            user_profile__latitude__isnull=False,
            user_profile__longitude__isnull=False,
            user_profile__latitude__range=(latitude_min, latitude_max),
            user_profile__longitude__range=(longitude_min, longitude_max),
            services__id=selected_service_id
        )

        return render(request, 'bookings/search_results.html', {'nearby_shops': nearby_shops})
def book_service(request, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    user_id = request.user.id if request.user.is_authenticated else None
    selected_service_id = request.session.get('selected_service_id')
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')

    if selected_service_id:
        selected_service = Service.objects.get(pk=selected_service_id)
        # Pass selected_service to the form when initializing it
        form = BookServiceForm(shop=shop, selected_service=selected_service)
    else:
        selected_service = None
        form = BookServiceForm(shop=shop)

    if request.method == 'POST':
        form = BookServiceForm(shop=shop, data=request.POST)
        if form.is_valid():
            book_service = form.save(commit=False)
            book_service.user_id = user_id
            book_service.shop = shop
            book_service.latitude = latitude
            book_service.longitude = longitude
            book_service.location = request.POST.get('location')
            book_service.time = request.POST.get('date')  # Assuming user selects date/time
            book_service.services = selected_service  # Assign selected_service here
            book_service.save()
            messages.success(request, 'Service booked successfully.')
            return redirect('index')
        else:
            print(form.errors)
            print(request.POST) 
    
    return render(request, 'bookings/book_service.html', {'shop': shop, 'form': form, 'selected_service': selected_service})


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
        'booking': booking
    }
    return render(request, 'bookings/rate_booking.html', context)
# views.py
from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404, render, redirect
from products.models import Product
from .models import Invoice, BookService

def create_invoice(request, booking_id):
    booking = get_object_or_404(BookService, id=booking_id)
    
    if hasattr(booking, 'invoice'):
        return HttpResponseRedirect(reverse('invoice_detail', args=[booking.invoice.id]))
    
    if request.method == 'POST':
        service_hours = int(request.POST.get('service_hours', 0))
        product_ids = request.POST.getlist('products')
        product_quantities = request.POST.getlist('product_quantities')
        total_amount_str = request.POST.get('total_amount', '0')
        
        try:
            total_amount = Decimal(total_amount_str)
        except InvalidOperation:
            total_amount = Decimal('0')
        
        invoice = Invoice.objects.create(
            booking=booking,
            service_hours=service_hours,
            total_amount=total_amount
        )
        
        for product_id, quantity in zip(product_ids, product_quantities):
            if product_id and quantity:
                product = Product.objects.get(id=product_id)
                invoice_product = InvoiceProduct.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=int(quantity)
                )
        
        return HttpResponseRedirect(reverse('invoice_detail', args=[invoice.id]))
    else:
        products = Product.objects.filter(user=booking.shop)
        return render(request, 'mechanicShop/create_invoice.html', {'booking': booking, 'products': products})
    
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, 'mechanicShop/invoice_detail.html', {'invoice': invoice})