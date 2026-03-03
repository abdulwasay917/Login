from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    identifier = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ForgotPasswordForm(forms.Form):
    username = forms.CharField()



