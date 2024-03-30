
from Accounts.models import UserProfile
from mechanic_shop.models import Shop

def get_shop(request):
    try:
        shop = Shop.objects.get(user=request.user)
    except:
        shop = None
    return dict(shop=shop)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)