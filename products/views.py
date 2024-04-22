import json
import uuid
from django.contrib import messages
from django.db.models import F

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from cart.cart import Cart
from django.urls import reverse
import requests

from .models import ProductPayment, PurchasedProduct

from Accounts.views import check_role_customer, check_role_shop
from mechanic_shop.models import Shop
from .models import Product
from django.shortcuts import render, redirect
from .forms import ProductForm



@user_passes_test(check_role_shop)
@login_required(login_url="login")
def productDetail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'cart/productDetail.html', {'product': product})

@login_required(login_url="login")
def cart_add(request, id):
    product = Product.objects.get(id=id)
    if product.availability <= 0:
        messages.error(request, "Product is currently out of stock. Select Others")
        return redirect('show_products')
    cart = Cart(request)
    request.session['product']=id
    request.session.save()
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

def user_orders(request):
    # Retrieve the ProductPayment instances for the logged-in user
    user_orders = ProductPayment.objects.filter(user=request.user).order_by('-payment_date')

    # Create a list to store details of each order
    orders_info = []

    # Iterate through each ProductPayment instance
    for order in user_orders:
        # Retrieve the PurchasedProduct instances associated with the current order
        purchased_products = PurchasedProduct.objects.filter(payment=order)

        # Create a list to store details of purchased products in the current order
        products_info = []

        # Iterate through each PurchasedProduct instance
        for purchased_product in purchased_products:
            # Append details of the purchased product to the list
            product_info = {
                'product_name': purchased_product.product.product_name,
                'shop_name': purchased_product.shop.shop_name,
                'quantity': purchased_product.quantity,
                'price': purchased_product.product.price,
                'subtotal': purchased_product.quantity * purchased_product.product.price
            }
            products_info.append(product_info)

        # Append details of the current order to the orders_info list
        orders_info.append({
            'order_id': order.id,
            'order_date': order.payment_date,
            'total_amount': order.amount,
            'products_info': products_info
        })

    # Pass the orders_info list to the template for rendering
    return render(request, 'customers/myOrders.html', {'orders_info': orders_info, 'current_page': "My Orders",
})


@login_required(login_url="login")
def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    return_url = 'http://localhost:8000/products/verify/'
    website_url = 'http://localhost:8000'
  
    user_obj=request.user
    # product_id = request.session.get('product')
    # product=Product.objects.get(id=product_id)
    # shop_id=product.user.id
    # shop=Shop.objects.get(id=shop_id)
    # print(shop)
    # print(product)
    
    cart = Cart(request)
    product_info=[]
    for key,value in request.session.get('cart', {}).items():
        product = Product.objects.get(pk=key)
        shop_id= product.user.id
        shop=Shop.objects.get(pk=shop_id)


        product_infos = {
             'id':product.pk,
            #  'name': product.product_name,
             'price': product.price,
             'quantity': value['quantity'],
             'shop': shop
        }
        product_info.append(product_infos)
   
   
    total_bill = 0
    for key, value in request.session['cart'].items():
        total_bill += float(value['price']) * value['quantity']
    
    # Store total bill in session
    cart_total_amount=total_bill	


    purchase_order_id = str(uuid.uuid4())  # Generating UUID for purchase order ID


    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": cart_total_amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "hlo",
        "customer_info": {
            "name": user_obj.name,
            "email":user_obj.email,
            "phone":user_obj.phone_number,
        }
    })

    # put your own live secret for admin
    headers = {
        'Authorization': 'key c66e09100007469f8bc80c31e921522f',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    new_res = json.loads(response.text)
   
    return redirect(new_res['payment_url'])

@login_required(login_url="login")
def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key c66e09100007469f8bc80c31e921522f',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        data = json.dumps({
            'pidx': pidx
        })
        res = requests.request('POST', url, headers=headers, data=data)

        new_res = json.loads(res.text)
        print(new_res)

        user_obj = request.user
        cart = Cart(request)
        products_info = []
        total_amount = 0

        for key, value in request.session.get('cart', {}).items():
            product = Product.objects.get(pk=key)
            shop_id = product.user.id
            shop = Shop.objects.get(pk=shop_id)
            product_info = {
                'product': product,
                'shop': shop,
                'quantity': value['quantity']
            }
            products_info.append(product_info)
            total_amount += (product.price * value['quantity'])

        if new_res['status'] == 'Completed':
            # Create ProductPayment instance
            payment = ProductPayment.objects.create(user=user_obj, amount=total_amount)

            # Associate purchased products with the payment
            for product_info in products_info:
                purchased_product = PurchasedProduct.objects.create(
                    product=product_info['product'],
                    payment=payment,
                    shop=product_info['shop'],
                    quantity=product_info['quantity']
                )

                # Decrease the availability of the product
                Product.objects.filter(pk=product_info['product'].pk).update(
                    availability=F('availability') - product_info['quantity']
                )

            # Clear the cart after successful payment
            cart.clear()

            # Display success message to the user
            messages.success(request, "Payment Successful")

            # Redirect to some page (e.g., home page)
            return redirect('index')

    # If payment status is not 'Completed', or for any other error, redirect to the home page
    return redirect('index')