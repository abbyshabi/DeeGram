from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#from .forms import ImageForm,ProfileForm,CommentForm
from .models import Image,Profile,User,Comments
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    images = Image.objects.order_by('-date')
    profile = Profile.objects.order_by('-last_update')
     
    return render(request,'index.html',{"images":images,"profile":profile})
