from django import forms
from .models import Post, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = "__all__"
    

class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True)
  class Meta:
   model = User
   fields = ('username', 'email', 'password1', 'password2')
    
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError("This email address is already in use.")
    return email



class UserProfileForm(forms.ModelForm):
  first_name= forms.CharField(required=False)
  last_name = forms.CharField(required=False)
  
  class Meta:
    model = UserProfile
    fields = ["dob", "gender", "pp"]

  #Validation Function
    #clean_<field_name>
  def clean_pp(self):
        image = self.cleaned_data.get('pp')

        if image:
        #Validate File Size (2MB max)
            if image.size > 1024 * 1024 * 2: #2MB
                raise ValidationError("Image size must be less than 2MB.")

          # Validate Extention
            ext = image.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise ValidationError("Only .jpg, .jpeg and .png files are allowed.")
            # Compress the Image
            img = Image.open(image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")  # Avoid PNG alpha channels causing large sizes

            output_io = io.BytesIO()
            img.save(output_io, format='JPEG', quality=50)

            output_io.seek(0)
            compressed_image = InMemoryUploadedFile(
                output_io,
                'ImageField',
                image.name,
                'image/jpeg',
                sys.getsizeof(output_io),
                None
            )
            return compressed_image
        
        return image