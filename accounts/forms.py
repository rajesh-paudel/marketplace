from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Vendor

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=("email","username")

class VendorForm(forms.ModelForm):
    class Meta:
        model=Vendor
        fields=("shop_name","description")        