from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
from products.models import ProductPayment
from bookings.models import BookService, Invoice
from .utils import detectUser, send_verification_email
from mechanic_shop.models import Service, Shop
from django.core.exceptions import PermissionDenied
from mechanic_shop.forms import ShopForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, UserProfile
from .forms import UserForm
from django.contrib.auth import login
from django.contrib import messages, auth
# Create your views here.

def check_role_shop(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            # Send Verification Email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered successfully! Verification link sent to Email')
            return redirect('login')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': UserForm,
    }
    return render(request, 'accounts/registerUser.html', context) 

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')


def registerShop(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        s_form = ShopForm(request.POST, request.FILES)
        if form.is_valid() and s_form.is_valid():
            print("Forms are valid")
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.MECHANIC_SHOP
            user.save()
            
            shop = s_form.save(commit=False)
            shop.user = user
            user_profile = UserProfile.objects.get(user=user)
            
            shop.user_profile = user_profile
            shop.save()  # Save the Shop instance first

            # Handle selected services
            services_ids = request.POST.getlist('services')
            selected_services = Service.objects.filter(id__in=services_ids)
            shop.services.set(selected_services)

            # Handle selected vehicle
            vehicle = request.POST.get('vehicles')
            shop.vehicles = vehicle
            shop.verification_status = 'pending' 
            shop.save()  # Save the Shop instance again after associating many-to-many relationships
            
            # Send Verification Email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered successfully! Verification link sent to Email. And Please wait for the approval to be listed in site as shop')
            return redirect('login')
        else:
            print(form.errors)
            print(s_form.errors) 
    else:
        form = UserForm()
        s_form = ShopForm()
    vehicle_choices = Shop._meta.get_field('vehicles').choices
    services = Service.objects.all()

    context = {
        'form': form,
        's_form': s_form,
        'services': services,
        'vehicle_choices': vehicle_choices,
    }
    return render(request, 'accounts/registerShop.html', context)

def custom_login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!!')
        return redirect('myAccount')
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
    
            return redirect('myAccount')
        else:
            if not User.objects.filter(email=email).exists():
                messages.error(request, "Invalid Email.")
            else:
                messages.error(request, "Incorrect Password.")
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged Out..')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    user = request.user
    
    # Get the current month
    current_month = datetime.now().month
    
    # Filter bookings for the current month
    bookings_this_month = BookService.objects.filter(user=user, created_at__month=current_month).count()
    
    # Get all bookings
    bookings = BookService.objects.filter(user=user)
    
    # Get the count of purchased orders
    purchased_orders_count = ProductPayment.objects.filter(user=user).count()

    return render(request, 'accounts/customerDashboard.html', {
        'bookings': bookings,
        'purchased_orders_count': purchased_orders_count,
        'bookings_this_month': bookings_this_month,
        'current_page': "Dashboard",
    })

@login_required(login_url='login')
@user_passes_test(check_role_shop)
def shopDashboard(request):
    shop = Shop.objects.get(user=request.user)
    bookings = BookService.objects.filter(shop=shop)

    # Calculate total booking revenues
    total_booking_revenues = Invoice.objects.filter(
        booking__shop=shop,
        payment_status='Paid'
    ).aggregate(total_amount=Sum('total_amount'))['total_amount']

    # If there is no revenue, set it to 0
    total_booking_revenues = total_booking_revenues if total_booking_revenues is not None else Decimal('0.00')

    # Get the current month's start and end dates
    current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month_start = current_month_start.replace(month=current_month_start.month + 1)
    current_month_end = next_month_start - timezone.timedelta(days=1)

    # Calculate the total booking revenue for this month
    total_booking_revenue_this_month = Invoice.objects.filter(
        booking__shop=shop,
        booking__date__gte=current_month_start,
        booking__date__lte=current_month_end,
        payment_status='Paid'
    ).aggregate(total_amount=Sum('total_amount'))['total_amount']

    # If there is no revenue for this month, set it to 0
    total_booking_revenue_this_month = total_booking_revenue_this_month if total_booking_revenue_this_month is not None else Decimal('0.00')

    return render(request, 'accounts/shopDashboard.html', {
        'total_booking_revenues': total_booking_revenues,
        'total_booking_revenue_this_month': total_booking_revenue_this_month,'bookings':bookings
    })

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset link has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate the user bu decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')
    

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
        
    return render(request, 'accounts/reset_password.html')
