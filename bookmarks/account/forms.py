from django import forms 


class LoginForm(forms.Form):
    """
    class auth for db
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) #vidget PasswordInpt can be use for unput type="password"
