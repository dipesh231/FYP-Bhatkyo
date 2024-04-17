from django.shortcuts import render
from bookings.models import RateBooking
from mechanic_shop.models import Service, Shop

from products.models import Product

# Create your views here.
def index(request):
    shops = Shop.objects.all()
    products = Product.objects.all()
    services = Service.objects.all()
    shop_reviews = RateBooking.objects.all()


    context = {
        'shops': shops,
        'products': products,
        'services':services,
        'shop_reviews': shop_reviews,
    }
    return render(request,"index.html",context)