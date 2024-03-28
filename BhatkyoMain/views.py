from django.shortcuts import render
from mechanic_shop.models import Shop

from products.models import Product

# Create your views here.
def index(request):
    shops = Shop.objects.all()
    products = Product.objects.all()
    print(products)

    context = {
        'shops': shops,
        'products': products,
    }
    return render(request,"index.html",context)