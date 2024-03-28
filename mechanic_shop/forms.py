from django import forms

from .models import Shop 

class ShopForm(forms.ModelForm):
    shop_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    shop_lisence = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

    class Meta:
        model = Shop 
        fields = ['shop_name', 'shop_image','shop_lisence', 'services','shop_location', 'vehicles', 'latitude', 'longitude']
        