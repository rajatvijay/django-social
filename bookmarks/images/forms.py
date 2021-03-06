from django import forms
from .models import Image
from urllib import urlopen
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ('title', 'url', 'description')
    widgets = {
      'url': forms.HiddenInput,
    }
  
  # We allow only .jpg and .jpeg  
  def clean_url(self):
    url = self.cleaned_data['url']
    valid_extensions = ['jpg', 'jpeg']
    extension = url.rsplit('.', 1)[1].lower()
    
    if extension not in valid_extensions:
      raise forms.ValidationError('The given URL does not match valid image extensions.')
    
    return url
    
  # We download image using the url provided bby the user
  def save(self, force_insert=False, force_update=False, commit=True):
    
    # crate an instance of the Image model but dont save it to the db
    image_instance = super(ImageCreateForm, self).save(commit=False)
    
    image_url = self.cleaned_data['url']
    image_name = '{}.{}'.format(slugify(self.cleaned_data['title']), image_url.rsplit('.', 1)[1])
    
    # download the image form the given url
    response = urlopen(image_url)
    
    # save the image with its name in the image field of the saved instance
    # but dont save the instance to the db
    image_instance.image.save(image_name, ContentFile(response.read()), save=False)
    
    if commit:
      image_instance.save()
      
    return image_instance
