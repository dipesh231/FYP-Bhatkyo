from django.shortcuts import render

from mechanic_shop.models import Shop

def Sprofile(request):
    shop = Shop.objects.get(user=request.user)
    context = {
        'shop': shop,
        'current_page': "My Shop",
    }
    return render(request, 'mechanicShop/sprofile.html', context)