from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, LoginForm, AddCourseForm
from django.contrib.auth.models import User
from .models import Profile, Course, CourseMaterial
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from datetime import datetime, timezone
from django.utils import timezone

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
            if user_image is None:
                user_image = "profile_pics/default.png"
                if password != confirmPassword:
                    form.add_error('confirm_password', 'Passwords do not match!')
                else:
                    user = User.objects.create_user(first_name=firstName, last_name=lastName, username=userName, email=email, password=password)
                    profile = Profile(user_type=typeof_user, phone=phone, user_image=user_image, user=user)
                    profile.save()
                    return redirect('index')
            else:
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
            if user is not None:
                auth_login(request, user)
                return redirect('home', user_id=user.pk)
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
def home(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    courses = Course.objects.filter(profile=profile)
    print(courses)
    context = {'user': user, 'profile': profile, 'courses': courses}
    return render(request, 'elearn_app/home.html', context)

def add_course(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    if profile.user_type == 'student':
        return HttpResponse('You are a student, you can not add a course.')
    else:
        if request.method == 'POST':
            form = AddCourseForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data['name']
                category = form.cleaned_data['category']
                description = form.cleaned_data['description']
                image = form.cleaned_data.get('image')
                created_at = timezone.now()
                course = Course.objects.create(name=name, category=category, description=description, created_at=created_at, image=image, profile=profile)
                course.save()
                messages.success(request, 'Your course has been added!')
                return redirect('home', user_id=user.pk)
        else:
            form = AddCourseForm()
        context = {'form': form}
        return render(request, 'elearn_app/add_course.html', context)
