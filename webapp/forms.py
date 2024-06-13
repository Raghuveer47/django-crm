from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Record, Invoice, ItemDetail

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
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autofocus': True,
        'id': 'id_username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'id_password'
    }))

class RecordForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'id_email'
    }))
    
    class Meta:
        model = Record
        fields = ['firstname', 'lastname', 'email', 'phone', 'city', 'college']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_firstname'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_lastname'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_phone'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_city'}),
            'college': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_college'}),
        }

class UpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'id_email'
    }))
    
    class Meta:
        model = Record
        fields = ['firstname', 'lastname', 'email', 'phone', 'city', 'college']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_firstname'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_lastname'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_phone'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_city'}),
            'college': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_college'}),
        }

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'id_csv_file'}))
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_no', 'billed_to_name', 'billed_to_email', 'description', 'date', 'order_no', 'gst_amount', 'total_amount']
        widgets = {
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
            'billed_to_name': forms.TextInput(attrs={'class': 'form-control'}),
            'billed_to_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'order_no': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ItemDetailForm(forms.ModelForm):
    class Meta:
        model = ItemDetail
        fields = ['name', 'price', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

ItemDetailFormSet = inlineformset_factory(Invoice, ItemDetail, form=ItemDetailForm, extra=1)
