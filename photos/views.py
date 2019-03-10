from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ImageForm,ProfileForm,CommentForm
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

@login_required(login_url='/accounts/login/')
def image(request,image_id):

    image = Image.objects.get(id = image_id)
    comments = Comments.get_comments_by_images(image_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.author = request.user
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()

    is_liked = False
    if image.likes.filter(id = request.user.id).exists():
        is_liked = True
    
    return render(request,"image.html", {"image":image,"is_liked":is_liked,"total_likes":image.total_likes(),'comments':comments,'form':form})

@login_required(login_url='/accounts/login/')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.poster= current_user
            image.save()
        return redirect('home')
    else:
        form = ImageForm()

    return render(request,'new_image.html',{'form':form})

@login_required(login_url='/accounts/login/')
def profile(request):
    user = request.user
    #profile = Profile.objects.get(user_id=current_user.id)
    images = Image.objects.all().filter(poster_id=user.id)
    return render(request, 'profile.html',{"user":user, "current_user":request.user,"images":images})

@login_required(login_url='/accounts/login/')
def user_profile(request,username):
    profile = User.objects.get(username=username)
    profile_details = Profile.get_by_id(profile.id)
    
    images = Image.get_profile_images(profile.id)
    
    is_followed = False
    if profile.follows.filter(id=request.user.id).exists():
        is_followed = True

    return render(request, 'user_profile.html', { 'profile':profile, 'profile_details':profile_details, 'images':images,'is_followed':is_followed})

@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect ('profile')
    else:
        form = ProfileForm()
    
    return render(request,'update_profile.html',{"form":form})