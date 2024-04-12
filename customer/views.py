from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test

from Accounts.forms import UserInfoForm, UserProfileForm
from Accounts.models import UserProfile
from Accounts.views import check_role_customer
from bookings.models import BookService

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
        'current_page': "Bookings",
    }
    return render(request, 'customers/myBookings.html', context)
