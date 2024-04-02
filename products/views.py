import json
import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import requests

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
def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = 'http://localhost:8000/products/khalti-init'
    website_url = 'http://localhost:8000'
    amount = str('1000')
    purchase_order_id = str(uuid.uuid4())  # Generating UUID for purchase order ID

    print("url", url)
    print("return_url", return_url)
    print("web_url", website_url)
    print("amount", amount)
    print("purchase_order_id", purchase_order_id)
    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "hlo",
        "customer_info": {
            "name": "{user.name}",
            "email": "test@khalti.com",
            "phone": "9800000001"
        }
    })

    # put your own live secret for admin
    headers = {
        'Authorization': 'key c66e09100007469f8bc80c31e921522f',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(json.loads(response.text))

    print(response.text)
    new_res = json.loads(response.text)
    # print(new_res['payment_url'])
    print(type(new_res))
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
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
           print("Payment completed successfully!")  # Print message in terminal
           cart = Cart(request)
           cart.clear()
            # If you want to display a message to the user, you can redirect to a page
            # or return an HTTP response with a message
        return HttpResponse("Payment completed successfully!")

    return redirect('index')