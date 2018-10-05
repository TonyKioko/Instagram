from django.shortcuts import render, redirect
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
