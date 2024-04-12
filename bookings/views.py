from datetime import datetime
from decimal import Decimal
import math
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from Accounts.views import check_role_customer
from products.models import Product
from .models import Invoice, InvoiceProduct, InvoiceService, RateBooking, BookService
from .forms import BookServiceForm
from django.shortcuts import render
from mechanic_shop.models import Service, Shop
from django.db.models import F
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test


def pinpoint_address(request):
    services = Service.objects.all()
    return render(request, 'bookings/search_form.html', {'services': services})

def nearby_shops(request):
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        selected_services_ids = request.POST.getlist('services')
        radius = int(request.POST.get('radius'))

        # Store selected services IDs and radius in session
        request.session['selected_services_ids'] = selected_services_ids
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        request.session['radius'] = radius

        # Convert radius to degrees
        radius_degrees = radius / 111  # 1 degree is approximately 111 kilometers

        # Calculate latitude and longitude ranges
        latitude_min = latitude - radius_degrees
        latitude_max = latitude + radius_degrees
        longitude_range = radius_degrees / abs(math.cos(math.radians(latitude)))
        longitude_min = longitude - longitude_range
        longitude_max = longitude + longitude_range

        # Query nearby shops
        nearby_shops = Shop.objects.filter(
            user_profile__latitude__isnull=False,
            user_profile__longitude__isnull=False,
            user_profile__latitude__range=(latitude_min, latitude_max),
            user_profile__longitude__range=(longitude_min, longitude_max)
        )

         # If only one service is selected, filter shops to include only those that offer that service
        if len(selected_services_ids) == 1:
            nearby_shops = nearby_shops.filter(services__id__in=selected_services_ids)
        # If multiple services are selected, filter shops to include only those that offer all selected services
        elif len(selected_services_ids) > 1:
            nearby_shops = nearby_shops.filter(services__id__in=selected_services_ids).annotate(num_services=Count('services')).filter(num_services=len(selected_services_ids))

        return render(request, 'bookings/search_results.html', {'nearby_shops': nearby_shops})

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def book_service(request, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')

    user_id = request.user.id if request.user.is_authenticated else None
    selected_services_ids = request.session.get('selected_services_ids', [])
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')

    selected_services = Service.objects.filter(pk__in=selected_services_ids)

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
            book_service.save()
            book_service.services.set(selected_services)  # Assign selected_service here
            messages.success(request, 'Service booked successfully.')
            return redirect('index')
        else:
            print(form.errors)
            print(request.POST)
    else:
        form = BookServiceForm(shop=shop, selected_services=selected_services)

    return render(request, 'bookings/book_service.html', {'shop': shop, 'form': form, 'selected_services': selected_services, 'current_date': current_date})


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
        service_ids = request.POST.getlist('services')  # Get list of selected service IDs
        service_hours = request.POST.getlist('service_hours')
        product_ids = request.POST.getlist('products')
        product_quantities = request.POST.getlist('product_quantities')
        total_amount_str = request.POST.get('total_amount', '0')
        
        try:
            total_amount = Decimal(total_amount_str)
        except InvalidOperation:
            total_amount = Decimal('0')
        
        invoice = Invoice.objects.create(
            booking=booking,
            total_amount=total_amount
        )
        for service_id, hours in zip(service_ids, service_hours):
            service = Service.objects.get(id=service_id)
            invoice_service = InvoiceService.objects.create(
                invoice=invoice,
                service=service,
                hours=int(hours)
            )
        
        for product_id, quantity in zip(product_ids, product_quantities):
             if product_id:  # Check if product ID is provided
                product = Product.objects.get(id=product_id)
                invoice_product = InvoiceProduct.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=int(quantity) if quantity else 0  # Set quantity to 0 if not provided
                )
                product.availability -= int(quantity)
                product.save()
        messages.success(request, 'Invoice Created successfully.')

        return HttpResponseRedirect(reverse('invoice_detail', args=[invoice.id]))
    else:
        products = Product.objects.filter(user=booking.shop)
        services = booking.services.all()
        return render(request, 'mechanicShop/create_invoice.html', {'booking': booking, 'products': products, 'services': services})

def invoice_detail(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    invoice_products = InvoiceProduct.objects.filter(invoice=invoice)
    
    # Calculate service total
    service_total = 0
    invoice_services = InvoiceService.objects.filter(invoice=invoice)
    for invoice_service in invoice_services:
        service_total += invoice_service.get_total_price()

    # Calculate product total
    product_total = 0
    for invoice_product in invoice_products:
        invoice_product.total = invoice_product.product.price * invoice_product.quantity
        product_total += invoice_product.total
    
    context = {
        'invoice': invoice,
        'invoice_products': invoice_products,
        'invoice_services':invoice_services,
        'product_total': product_total,
        'service_total': service_total
    }

    return render(request, 'mechanicShop/invoice_detail.html', context)
