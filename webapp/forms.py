from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Record ,CashReceipt, ProductDetail
from django.forms import inlineformset_factory

from .models import CashReceipt

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'id_email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'id_username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'id_password1'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'id_password2'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

#Create record
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['firstname', 'lastname', 'email', 'phone', 'city', 'college']

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['firstname', 'lastname', 'email', 'phone', 'city', 'college']
# forms.py
from django import forms

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()



class CashReceiptForm(forms.ModelForm):
    class Meta:
        model = CashReceipt
        fields = ['recipient_name', 'recipient_email', 'receipt_number', 'amount', 'gst_amount', 'total_amount', 'description']

ProductDetailFormSet = inlineformset_factory(CashReceipt, ProductDetail, fields=('name', 'price', 'quantity'), extra=1)