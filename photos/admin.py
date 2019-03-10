from django.contrib import admin
from .models import Image,Location,Comments,Profile
# Register your models here.

admin.site.register(Image)
admin.site.register(Location)
admin.site.register(Comments)
admin.site.register(Profile)