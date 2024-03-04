from django.http import HttpResponse
from django.shortcuts import redirect, render
from mechanic_shop.models import Service, Shop

from mechanic_shop.forms import ShopForm

from .models import User, UserProfile
from .forms import UserForm
from django.contrib import messages
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
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
    if request.method == 'POST':
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