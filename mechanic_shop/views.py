from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test

from Accounts.forms import UserForm, UserProfileForm
from Accounts.models import User, UserProfile
from Accounts.views import check_role_shop
from bookings.models import BookService
from mechanic_shop.forms import  ShopForm
from mechanic_shop.models import Service, Shop
@login_required(login_url='login')
@user_passes_test(check_role_shop)
def Sprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    shop = get_object_or_404(Shop, user=request.user)
    vehicle_choices = Shop._meta.get_field('vehicles').choices
    services = Service.objects.all()

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        shop_form = ShopForm(request.POST, request.FILES, instance=shop)
        if profile_form.is_valid() and shop_form.is_valid():
            # Save the profile and shop forms
            profile_form.save()
            shop = shop_form.save(commit=False)
            
            # Update latitude and longitude fields
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                # Validate latitude and longitude values
                try:
                    latitude = float(latitude)
                    longitude = float(longitude)
                    profile.latitude = latitude
                    profile.longitude = longitude
                    profile.save()
                    messages.success(request, 'Shop is Updated')
                    return redirect('sprofile')
                except ValueError:
                    messages.error(request, 'Invalid latitude or longitude values.')
            else:
                messages.error(request, 'Latitude or longitude values are missing.')
        else:
            messages.error(request, 'Form validation failed.')
            print(profile_form.errors)
            print(shop_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        shop_form = ShopForm(instance=shop)

    context = {
        'profile_form': profile_form,
        'shop_form': shop_form,
        'profile': profile,
        'shop': shop,
        'services': services,
        'vehicle_choices': vehicle_choices,
    }
    return render(request, 'mechanicShop/sprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_shop)
def Bookings(request):
    shop = Shop.objects.get(user=request.user)
    bookings = BookService.objects.filter(shop=shop)
    context = {
        'shop':shop,
        'bookings': bookings,
        'current_page': "Bookings",
    }
    return render(request, 'mechanicShop/bookings.html', context)
@login_required(login_url='login')
@user_passes_test(check_role_shop)
def delete_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(BookService, id=booking_id)
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
    return redirect('bookings')

def booking_details(request, booking_id):
    booking = get_object_or_404(BookService, id=booking_id)
    return render(request, 'mechanicShop/booking_details.html', {'booking': booking})
