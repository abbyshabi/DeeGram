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