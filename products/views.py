import json
import uuid
from django.contrib import messages

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from cart.cart import Cart
import requests

from .models import ProductPayment
from django.core.paginator import Paginator

from Accounts.views import check_role_shop
from mechanic_shop.models import Shop
from .models import Product
from django.shortcuts import render, redirect
from .forms import ProductForm


def show_products(request):
    products_list = Product.objects.all()  # Fetch all products
    paginator = Paginator(products_list, 5)  # Show 10 products per page

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'products/products.html', {'products': products})

@user_passes_test(check_role_shop)
@login_required(login_url="login")
def productDetail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'cart/productDetail.html', {'product': product})

@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
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
    # print(new_res['payment_url'])
   
    return redirect(new_res['payment_url'])
  
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
        product_info = []
        products = []

        for key, value in request.session.get('cart', {}).items():
            product = Product.objects.get(pk=key)
            products.append(key)
            shop_id = product.user.id
            shop = Shop.objects.get(pk=shop_id)
            product_infos = {
                'id': product.pk,
                'name': product.product_name,
                'price': product.price,
                'quantity': value['quantity'],
                'shop': shop
            }
            product_info.append(product_infos)
        print(product_info)

        total_bill = 0
        for key, value in request.session['cart'].items():
            total_bill += float(value['price']) * value['quantity']
        print(new_res['status'])
        if new_res['status'] == 'Completed':
            selected_products = Product.objects.filter(pk__in=products)
            pay = ProductPayment.objects.create(user=request.user, amount=total_bill)
            pay.product.set(selected_products)
            pay.save()
            print(pay)
            print("Payment completed successfully!")

            cart = Cart(request)
            cart.clear()
            messages.success(request, "Payment Successful")  # Print message in terminal
            return redirect('index')
            # If you want to display a message to the user, you can redirect to a page
            # or return an HTTP response with a message
    return redirect('index')
