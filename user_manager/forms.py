from django.contrib.auth.models import User
from django import forms


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control form-control-sm'}),
        }


class SignInForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm'}))

