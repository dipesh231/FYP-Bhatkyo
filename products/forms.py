# forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'description', 'total_quantity', 'availability', 'price', 'product_image']
