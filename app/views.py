from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from app.forms import *
from app.forms import SignupForm, ImageForm, ProfileForm, CommentForm

from django.contrib import messages
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from .emails import send_activation_email
from app.models import *

import smtplib



# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            to_email = form.cleaned_data.get('email')
            # send_activation_email(user, current_site, to_email)

            mail_subject = 'Activate your pixargram account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            # email.send()
            send_mail(mail_subject,message,'tonnibravo12@gmail.com',[to_email],fail_silently=False)

            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. ''<a href="/accounts/login/"> Now you can login to your account </a>''')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='/accounts/login/')
def index(request):
    images = Image.objects.order_by('-timestamp')
    comments = Comment.objects.order_by('-timestamp')
    profiles = Profile.objects.order_by('-timestamp')

    context ={"images":images,"comments":comments,"profiles":profiles}

    return render(request,'index.html',context)

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
    return render(request,'edit_profile.html',{"form":form})



@login_required(login_url='/accounts/login')
def user_profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    images = Image.objects.all().filter(user_id=user_id)
    return render(request, 'profile.html', {'profile':profile, 'images':images})
@login_required(login_url='/accounts/login/')
def profile(request, username):
    title = "Profile"
    profile = User.objects.get(username=username)
    comments = Comment.objects.all()
    users = User.objects.get(username=username)
    id = request.user.id
    # liked_images = Likes.objects.filter(user_id=id)
    # mylist = [i.image_id for i in liked_images]
    form = CommentForm()

    try :
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)


    images = Image.get_profile_pic(profile.id)
    return render(request, 'profile/profile.html', {'title':title, 'comments':comments,'profile':profile, 'profile_details':profile_details, 'images':images, 'follow':follow, 'following':following, 'list':mylist,'people_following':people_following,'form':form})

@login_required(login_url='/accounts/login')
def new_image(request):
	current_user = request.user
	if request.method == 'POST':
		form = ImageForm(request.POST,request.FILES)
		if form.is_valid():
			new_image = form.save(commit=False)
			new_image.user = current_user
			new_image.save()
            # messages.success(request, "Image uploaded!")
			return redirect('index')
	else:
			form = ImageForm()
	return render(request, 'new_image.html',{"form":form })


@login_required(login_url='/accounts/login/')
def comment(request,image_id):
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

@login_required (login_url='/accounts/register/')
def like_photo(request,id):
    image = Image.objects.get(id=id)
    image.likes = image.likes + 1
    image.save()
    return redirect('index')

@login_required(login_url='/accounts/login')
def image_details(request,id):
    image = Image.objects.get(id = id)
    comments = Comment.objects.order_by('-timestamp')

    context={"image":image,"comments":comments}
    return render(request, 'image_details.html',context)


def search_results(request):

    # if 'caption' in request.GET and request.GET["caption"]:
    if 'username' in request.GET and request.GET["username"]:

        search_term = request.GET.get("username")
        found_users = Profile.search_by_username(search_term)
        message = f"{search_term}"
        print(search_term)

        context = {"users":found_users,"message":message}

        return render(request, 'search.html',context)

    else:
        message = "You haven't searched for any term"
        # context={"message":message}
        return render(request, 'search.html',{"message":message})
