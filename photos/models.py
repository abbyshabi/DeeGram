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

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile
    
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile

    def get_absolute_url(self): 
        return reverse('user_profile')
    

class Image(models.Model):
   """
   This is the class we will use to create images
   """
   image_url = models.ImageField(upload_to = "images/")
   name = models.CharField(max_length = 30)
   caption = HTMLField()
   poster = models.ForeignKey(User,related_name='images')
   likes = models.ManyToManyField(User, related_name='likes' ,blank = True)
   date = models.DateTimeField(auto_now_add = True,null = True)


class Comments(models.Model):
    text = models.CharField(max_length = 100, blank = True)
    image = models.ForeignKey(Image, related_name = "comments")
    author = models.ForeignKey(User, related_name = "author")
    created_date = models.DateTimeField(auto_now_add = True,null = True)
    approved_comment = models.BooleanField(default=False)
 