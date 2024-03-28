
from mechanic_shop.models import Shop

def get_shop(request):
    try:
        shop = Shop.objects.get(user=request.user)
    except:
        shop = None
    return dict(shop=shop)