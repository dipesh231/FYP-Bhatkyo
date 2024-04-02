from django import forms
from .models import  Shop 

class ShopForm(forms.ModelForm):
    shop_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    shop_lisence = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

    class Meta:
        model = Shop 
        fields = ['shop_name', 'shop_image','shop_lisence', 'services', 'vehicles']

# class BillForm(forms.ModelForm):
#     class Meta:
#         model = ServiceBill
#         fields = ['user', 'shop', 'service', 'hours', 'total_price', 'products_used']

#     def __init__(self, *args, **kwargs):
#         super(BillForm, self).__init__(*args, **kwargs)
#         self.fields['user'].widget = forms.HiddenInput()
#         self.fields['shop'].widget = forms.HiddenInput()
#         self.fields['total_price'].widget = forms.NumberInput(attrs={'readonly': 'readonly'})
