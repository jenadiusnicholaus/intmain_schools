from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm

from authentication.models import Profile



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

from django.contrib.auth.forms import PasswordResetForm

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)



class SetPasswordForm(SetPasswordForm):
    new_password1 =forms.CharField(
        required=True,
        label='New password',
        help_text='Max-length:8 chars, not  smillar to username,strong one',
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))

    new_password2 =forms.CharField(
        required=True,
        label='Re-enter password',
        help_text='Max-length:8 chars, not smillar to username,strong one',
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Re-nter password'
    }))
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class singleUserProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control ',
        'rows': "2",
        'cols': "100",
        'placeholder': 'Write your bio here...',

    }))
    about = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your about here...',

    }))
    profession = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your profession here...',
    }))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your country name here...',
    }))
    facebook_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write your facebook link here...',
    }))

    linkedin_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write your linked link here...',
    }))
    tweeter_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write your tweeter link here...',
    }))
    github_link = forms.URLField(required=False,  widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write your github link here...',
    }))
    image = forms.FileField(required=False,  widget=forms.FileInput(attrs={
        'class': 'form-control',

    }))

    class Meta:
        model = Profile
        fields = ('image', 'bio', 'profession', 'country', 'about', 'facebook_link', 'linkedin_link', 'tweeter_link',
                  'github_link', 'career_goal')

class usersForm(forms.ModelForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your username here...',
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your email here...',
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your first name here...',
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your last name here...',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')