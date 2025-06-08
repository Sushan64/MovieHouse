from django.db import models
from django.utils.text import slugify
from froala_editor.fields import FroalaField
from django.contrib.auth.models import User

# Create your models here.
def generate_slug(instance):
  base_slug = slugify(instance.title)
  slug = base_slug
  num = 1
  while Post.objects.filter(slug=slug).exists():
    slug = f"{base_slug}-{num}"
    num += 1
    return slug
  return base_slug
  
class Post(models.Model):
  title = models.CharField(max_length = 300)
  featured_image = models.ImageField(upload_to = "featured/", null= True, blank = True)
  content = FroalaField()
  meta_description = models.TextField(max_length = 250)
  slug = models.SlugField(max_length=300, null= True, blank = True, unique = True)
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = generate_slug(self)
    super().save(*args, **kwargs)
  
  def __str__(self):
    return self.title


class UserProfile(models.Model):
  GENDER_CHOICE = {
    'M': 'Male',
    'F': 'Female',
    'O' : 'Others',
  }
  user= models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
  pp = models.ImageField(upload_to="pp/", null=True, blank=True)
  gender = models.CharField(max_length=1, null=True, choices=GENDER_CHOICE, blank=True)
  dob = models.DateField(null=True, blank=True)
  
  def __str__(self):
    return str(self.user)