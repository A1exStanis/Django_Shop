from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class LogoutForm(forms.Form):
    pass


class NewUserForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'focus:outline-none',
        'placeholder': 'Enter your name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'focus:outline-none',
        'placeholder': 'mail@mail.com'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'focus:outline-none',
        'placeholder': 'Enter your password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'focus:outline-none',
        'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
