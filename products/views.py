from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from Bhatkyo import settings

from .models import Product
import stripe

# Create your views here.
@login_required(login_url="login")
def productDetail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'cart/productDetail.html', {'product': product})

@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

@login_required(login_url="login")
def Checkout(request):
    # Retrieve cart details
    cart_items = request.session.get('cart', {})
    line_items = []

    # Create line items for each product in the cart
    for product_id, quantity in cart_items.items():
        product = Product.objects.get(id=product_id)
        line_items.append({
            'price_data': {
                'currency': 'npr',  # Adjust currency as needed
                'unit_amount': int(product.price * 100),  # Convert price to cents
                'product_data': {
                    'name': product.product_name,
                      # Adjust image URL field as needed
                },
            },
            'quantity': quantity,
        })
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )
        return JsonResponse({'sessionId': session['id']})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)
    