# forms.py

from django import forms
from .models import BookService

class BookServiceForm(forms.ModelForm):
    class Meta:
        model = BookService
        fields = ['services', 'vehicles', 'problem_description','location','time']
        widgets = {
            'user_id': forms.HiddenInput(),
            'shop_name': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, shop, *args, **kwargs):
        super(BookServiceForm, self).__init__(*args, **kwargs)
        self.fields['services'].queryset = shop.services.all()
        self.initial['shop'] = shop
