from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test

from Accounts.forms import UserInfoForm, UserProfileForm
from Accounts.models import UserProfile
from Accounts.views import check_role_customer
from bookings.models import BookService, Invoice, InvoiceProduct, InvoiceService

# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def Cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Details is Updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
        'current_page': "Profile",
    }
    return render(request, 'customers/cprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def myBookings(request):
    bookings = BookService.objects.filter(user=request.user)
    for booking in bookings:
        booking.selected_services = booking.services.all() 
    context = {
        'bookings': bookings,
        'current_page': "My Bookings",
    }
    return render(request, 'customers/myBookings.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def my_booking_details(request, booking_id):
    booking = get_object_or_404(BookService, id=booking_id)
    shop = booking.shop
    return render(request, 'customers/booking_details.html', {'booking': booking, 'shop':shop})

@user_passes_test(check_role_customer)
def view_invoice_detail(request, invoice_id):
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

    return render(request, 'customers/my_invoice_detail.html', context)

@user_passes_test(check_role_customer)
def mark_as_paid(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        invoice.payment_status = 'Paid'
        invoice.save()
        # Redirect to the invoice detail page
        return redirect('view_invoice_detail', invoice_id=invoice_id)
    return redirect('view_invoice_detail', invoice_id=invoice_id)  # Redirect back to invoice detail page if not POST request
