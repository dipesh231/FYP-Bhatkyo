from django.shortcuts import render
from bookings.models import BookService, RateBooking
from mechanic_shop.models import Service, Shop
from django.core.paginator import Paginator

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

def aboutUs(request):
    booking_count = BookService.objects.count()
    shop_count = Shop.objects.count()
    service_count = Service.objects.count()
    rating_users_count = RateBooking.objects.values('user').distinct().count()

    context = {
        'shop_count': shop_count,
        'service_count':service_count,
        'booking_count': booking_count,
        'rating_users_count': rating_users_count,
    }
    return render(request,"aboutus.html",context)

def contact(request):
    return render(request, 'contact.html')

def show_products(request):
    query = request.GET.get('q')
    products_list = Product.objects.all()  # Fetch all products

    if query:
        products_list = products_list.filter(
            product_name__icontains=query
        )

    paginator = Paginator(products_list, 5)  # Show 5 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'search_term': query,
    }
    return render(request, 'products/products.html', context)

