from django.shortcuts import render
from mechanic_shop.models import Service, Shop

from products.models import Product

# Create your views here.
def index(request):
    shops = Shop.objects.all()
    products = Product.objects.all()
    services = Service.objects.all()
    print(products)

    context = {
        'shops': shops,
        'products': products,
        'services':services,
    }
    return render(request,"index.html",context)