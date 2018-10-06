from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.forms import *




# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    return render(request,'index.html',{})

@login_required(login_url='/accounts/login/')
def new_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = current_user
            update.save()
            return redirect('index')
    else:
        form = ProfileForm()
    return render(request,'profile.html',{"form":form})

@login_required(login_url='/accounts/login')
def new_image(request):
	current_user = request.user
	if request.method == 'POST':
		form = ImageForm(request.POST,request.FILES)
		if form.is_valid():
			new_image = form.save(commit=False)
			new_image.user = current_user
			new_image.save()
			return redirect('index')
	else:
			form = ImageForm()
	return render(request, 'new_image.html',{"form":form })


@login_required(login_url='/accounts/login/')
def new_comment(request,image_id):
    image = get_object_or_404(Image, pk=image_id)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = current_user
            comment.save()
            return redirect('index')
    else:
        form = CommentForm()
    return render(request, 'comment.html', {"user":current_user,"form":form})
