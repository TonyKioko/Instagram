from django import forms
from app.models import *
from django.contrib.auth.forms import UserCreationForm
# https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['user','profile','likes','timestamp']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
