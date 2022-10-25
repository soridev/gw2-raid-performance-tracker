from django import forms
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.PasswordInput()
