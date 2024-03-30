from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import BookService
from .utils import detectUser
from mechanic_shop.models import Service, Shop
from django.core.exceptions import PermissionDenied
from mechanic_shop.forms import ShopForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, UserProfile
from .forms import UserForm
from django.contrib import messages, auth
# Create your views here.

def check_role_shop(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': UserForm,
    }
    return render(request, 'accounts/registerUser.html', context) 

def registerShop(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        s_form = ShopForm(request.POST, request.FILES)
        if form.is_valid() and s_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.MECHANIC_SHOP
            user.save()
            
            shop = s_form.save(commit=False)
            shop.user = user
            user_profile = UserProfile.objects.get(user=user)
            shop.user_profile = user_profile
            shop.save()  # Save the Shop instance first

            # Handle selected services
            services_ids = request.POST.getlist('services')
            selected_services = Service.objects.filter(id__in=services_ids)
            shop.services.set(selected_services)

            # Handle selected vehicle
            vehicle = request.POST.get('vehicles')
            shop.vehicles = vehicle
            shop.verification_status = 'pending' 
            shop.save()  # Save the Shop instance again after associating many-to-many relationships

            messages.success(request, 'Your account has been registered successfully! Please wait for the approval')
            return redirect('registerShop')
        else:
            print(form.errors)
    else:
        form = UserForm()
        s_form = ShopForm()
    vehicle_choices = Shop._meta.get_field('vehicles').choices
    services = Service.objects.all()

    context = {
        'form': form,
        's_form': s_form,
        'services': services,
        'vehicle_choices': vehicle_choices,
    }
    return render(request, 'accounts/registerShop.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in..")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid login Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged Out..')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    bookings = BookService.objects.filter(user=request.user)
    return render(request, 'accounts/customerDashboard.html',{'bookings': bookings})

@login_required(login_url='login')
@user_passes_test(check_role_shop)
def shopDashboard(request):
    shop = Shop.objects.get(user=request.user)
    bookings = BookService.objects.filter(shop=shop)
    context = {
        'shop': shop,
        'bookings': bookings,
        'current_page': "Dashboard",
    }
    return render(request, 'accounts/shopDashboard.html', context)


