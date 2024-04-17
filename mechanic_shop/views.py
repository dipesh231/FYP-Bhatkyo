from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test

from Accounts.forms import UserForm, UserProfileForm
from Accounts.models import User, UserProfile
from Accounts.views import check_role_shop
from chatapp.models import ChatRoom
from products.forms import ProductForm
from products.models import Product
from bookings.models import BookService, RateBooking
from mechanic_shop.forms import  ShopForm
from mechanic_shop.models import Service, Shop
@login_required(login_url='login')
@user_passes_test(check_role_shop)
def Sprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    shop = get_object_or_404(Shop, user=request.user)
    vehicle_choices = Shop._meta.get_field('vehicles').choices
    services = Service.objects.all()
    shop_reviews = RateBooking.objects.filter(book_service__shop=shop)


    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        shop_form = ShopForm(request.POST, request.FILES, instance=shop)
        if profile_form.is_valid() and shop_form.is_valid():
            # Save the profile and shop forms
            profile_form.save()
            shop_form.save()
            
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
        'shop_reviews': shop_reviews,
    }
    return render(request, 'mechanicShop/sprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_shop)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated:  # Check if user is authenticated
                shop = get_object_or_404(Shop, user=request.user)
                product = form.save(commit=False)
                product.user = shop  # Assign the shop to the product's user field
                product.save()
                return redirect('products')  # Redirect to product detail page after adding the product
            else:
                return redirect('login')  # Redirect to login page if user is not authenticated
    else:
        form = ProductForm()
    return render(request, 'mechanicShop/add_product.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(check_role_shop)
def Products(request):
    # Retrieve the shop associated with the logged-in user
    shop = get_object_or_404(Shop, user=request.user)
    
    # Filter products by the shop
    products = Product.objects.filter(user=shop)
    
    context = {
        'products': products
    }
    return render(request, 'mechanicShop/products.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_shop)
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'mechanicShop/productDetail.html', {'product': product})
from django.core.files.uploadedfile import InMemoryUploadedFile

@login_required(login_url='login')
@user_passes_test(check_role_shop)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if request.user.is_authenticated:
                shop = get_object_or_404(Shop, user=request.user)
                updated_product = form.save(commit=False)
                updated_product.user = shop
                updated_product.save()
                return redirect('product_detail', product_id=product_id)
            else:
                return redirect('login')
    else:
        form = ProductForm(instance=product)

    return render(request, 'mechanicShop/edit_product.html', {'form': form, 'product': product})

@login_required(login_url='login')
@user_passes_test(check_role_shop)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
    
        product.delete()
        messages.success(request, 'Product deleted successfully.')
            
    return redirect('products')  
   

@login_required(login_url='login')
@user_passes_test(check_role_shop)
def Bookings(request):
    shop = Shop.objects.get(user=request.user)
    bookings = BookService.objects.filter(shop=shop).order_by('-date')
    for booking in bookings:
        booking.selected_services = booking.services.all() 
    context = {
        'shop': shop,
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
