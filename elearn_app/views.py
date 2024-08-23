from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'elearn_app/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            firstName = form.cleaned_data['first_name']
            lastName = form.cleaned_data['last_name']
            userName = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirmPassword = form.cleaned_data['confirm_password']
            phone = form.cleaned_data['phone']
            typeof_user = form.cleaned_data['role']
            user_image = form.cleaned_data.get('user_image')
            if password != confirmPassword:
                form.add_error('confirm_password', 'Passwords do not match!')
            else:
                user = User.objects.create_user(first_name=firstName, last_name=lastName, username=userName, email=email, password=password)
                profile = Profile(user_type=typeof_user, phone=phone, user_image=user_image, user=user)
                profile.save()
                return redirect('index')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'authorization/signup.html', context)


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error('username', 'User does not exist!')
    else:
        form = LoginForm()
    context = {"form": form}
    return render(request, 'authorization/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('index')

@login_required
def home(request):
    users = User.objects.all()
    profiles = Profile.objects.all()
    context = {'users': users, 'profiles': profiles}
    return render(request, 'elearn_app/home.html', context)