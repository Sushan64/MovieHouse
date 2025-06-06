from django.db import models
from django.utils.text import slugify
from froala_editor.fields import FroalaField

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
  