from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from Accounts.forms import UserForm, UserProfileForm
from Accounts.models import UserProfile
from mechanic_shop.forms import ShopForm
from mechanic_shop.models import Service, Shop

@login_required
def Sprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    shop = get_object_or_404(Shop, user=request.user)
    vehicle_choices = Shop._meta.get_field('vehicles').choices
    services = Service.objects.all()
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        shop_form = ShopForm(request.POST, request.FILES, instance=shop)
        if profile_form.is_valid() and shop_form.is_valid():
            profile_form.save()
            shop_form.save()
            messages.success(request, 'Shop is Updated')
            return redirect('sprofile')
        else:
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
