from django import forms
from .models import BookService

class BookServiceForm(forms.ModelForm):
    location = forms.CharField(label='Location', required=True)  # Add location field

    class Meta:
        model = BookService
        fields = ['vehicles', 'problem_description', 'date', 'location']  # Include location field
        widgets = {
            'user_id': forms.HiddenInput(),
            'shop_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'services': forms.HiddenInput(),
        }

    def __init__(self, shop, location=None, latitude=None, longitude=None, selected_services=None, *args, **kwargs):
        super(BookServiceForm, self).__init__(*args, **kwargs)
        self.fields['vehicles'].queryset = shop.vehicle_choices
        self.initial['shop'] = shop
        self.initial['latitude'] = latitude
        self.initial['location'] = location
        self.initial['longitude'] = longitude

        if selected_services and selected_services in shop.services.all():
            self.initial['services'] = selected_services
        else:
            self.initial['services'] = None  # Reset the selected service if it doesn't belong to the shop

from .models import RateBooking

class RateBookingForm(forms.ModelForm):
    class Meta:
        model = RateBooking
        fields = ['rating', 'review']
