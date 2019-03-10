from django import forms
from django.core import validators
from .models import Image,Profile,Comments


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude=['likes','poster']