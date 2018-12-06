from django import forms
from djangotwitter.models import Author
from datetime import datetime


class SignupForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class PostForm(forms.Form):
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        current_user = Author.objects.filter(user=user).first()
        if current_user:
            self.fields['author'].choices = [(current_user.id, current_user.name)]
            

    body = forms.CharField(max_length=150)
    author = forms.ChoiceField()
    date = forms.DateTimeField(initial=datetime.now(), required=False)


