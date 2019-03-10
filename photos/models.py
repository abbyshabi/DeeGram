from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from tinymce.models import HTMLField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.template.defaultfilters import slugify


class Profile(models.Model):
    profile_image = models.ImageField(blank=True,upload_to='profiles/')
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    follows = models.ManyToManyField(User, related_name='follows' ,blank = True)

    def save_profile(self):
        self.save()
