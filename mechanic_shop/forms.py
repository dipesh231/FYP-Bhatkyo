from django import forms

from .models import Shop 

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop 
        fields = ['shop_name', 'shop_lisence', 'services','shop_location', 'vehicles', 'latitude', 'longitude']
        