from django import forms

from .models import User, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    address = forms.CharField(max_length = 50)
    profile_photo = forms.ImageField(required=False) 
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'phone_number', 'password', 'address', 'profile_photo']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password Does not Match!!"
            )

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address', 'lattitude', 'longitude']
                