from django import forms
from usuarios.models import Producto

class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['name', 'brand', 'price']

class EditProductForm(forms.ModelForm):
    sku = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Producto
        fields = ['sku', 'name', 'brand', 'price']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from usuarios.models import Profile


class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')


