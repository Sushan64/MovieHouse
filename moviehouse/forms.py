from django import forms
from .models import Post, UserProfile
from froala_editor.widgets import FroalaEditor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = "__all__"
    widgets = {
      'content': FroalaEditor(),
    }

class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField()
  class Meta:
   model = User
   fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
  first_name= forms.CharField(required=False)
  last_name = forms.CharField(required=False)
  
  class Meta:
    model = UserProfile
    fields = ["dob", "gender", "pp"]