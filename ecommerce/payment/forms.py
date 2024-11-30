from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    ship_full_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'full name'}), required=True)
    ship_email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email address'}), required=True)
    ship_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address1'}), required=True)
    ship_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address2'}), required=True)
    ship_city = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}), required=True)
    ship_state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}), required=True)
    ship_country = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}), required=True)
    ship_zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zip_code'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ('ship_full_name', 'ship_email', 'ship_address1', 'ship_address2', 'ship_city', 'ship_state', 'ship_country', 'ship_zipcode')
        exclude = ['user']