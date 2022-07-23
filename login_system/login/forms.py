from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(max_length=50, label = "name")
    ps = forms.CharField(widget=forms.PasswordInput(), label = "password")
    email_user = forms.EmailField(label="email", max_length=100)