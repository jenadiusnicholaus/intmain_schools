from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegitrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,  required=False,help_text='')
    last_name = forms.CharField(max_length=30, required=False, help_text='')
    username = forms.CharField(
        max_length=254, min_length=4, 
        help_text='You will use this info to login',
         widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    })
        )
    email = forms.EmailField(
        max_length=254,
        help_text='Enter a valid email address',
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email address'
    })
        )
        
    password1 =forms.CharField(
        label='Password',
        help_text='Max-length:8 chars, not  smillar to username,strong one',
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))
    password2 =forms.CharField(
        label='Confirm password',
        help_text='Must be similar to the one you entered before',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Re-enter password',
           'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30,  required=False,help_text='')
    last_name = forms.CharField(max_length=30, required=False, help_text='')
    email = forms.EmailField(
        max_length=254,
        help_text='Enter a valid email address',
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email address'
    })
        )
        
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]