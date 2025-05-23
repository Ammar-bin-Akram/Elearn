from django.shortcuts import render, redirect, HttpResponse
from .forms import ChangeProfilePictureForm, SignUpForm, LoginForm, AddCourseForm, AddCourseMaterialForm
from django.contrib.auth.models import User
from .models import Profile, Course, CourseMaterial, Enroll, CourseCompletionProgress, Rating
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from datetime import datetime, timezone
from django.utils import timezone
import string
import random

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
                    return redirect('login')
            else:
                if password != confirmPassword:
                    form.add_error('confirm_password', 'Passwords do not match!')
                else:
                    user = User.objects.create_user(first_name=firstName, last_name=lastName, username=userName, email=email, password=password)
                    user_image.name = custom_filename(user_image.name)
                    profile = Profile(user_type=typeof_user, phone=phone, user_image=user_image, user=user)
                    profile.save()
                    return redirect('login')
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
                return redirect('index')
            else:
                form.add_error('username', 'User does not exist!')
    else:
        form = LoginForm()
    context = {"form": form}
    return render(request, 'authorization/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')

@login_required
def home(request, user_id, category):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    courses = Course.objects.filter(profile=profile)
    if category == 'all':    
        all_courses = Course.objects.all()
        context = {'user': user, 'profile': profile, 'courses': courses, 'all_courses': all_courses}
        return render(request, 'elearn_app/home.html', context)
    else:
        all_courses = Course.objects.filter(category=category)
        context = {'user': user, 'profile': profile, 'courses': courses, 'all_courses': all_courses}
        return render(request, 'elearn_app/home.html', context)


@login_required
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
                if image is None:
                    image = 'course_pics/default.png'
                    course = Course.objects.create(name=name, category=category, description=description, created_at=created_at, image=image, profile=profile)
                    course.save()
                else:
                    image.name = custom_filename(image.name)
                    course = Course.objects.create(name=name, category=category, description=description, created_at=created_at, image=image, profile=profile)
                    course.save()
                messages.success(request, 'Your course has been added!')
                return redirect('home', user_id=user.pk, category='all')
        else:
            form = AddCourseForm()
        context = {'form': form, 'profile': profile}
        return render(request, 'elearn_app/add_course.html', context)
    

def view_course(request, user_id, course_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    if profile.user_type == 'teacher':
        course = Course.objects.get(pk=course_id)
        course_materials = CourseMaterial.objects.filter(course=course)
        context = {'user': user, 'course': course, 'profile': profile, 'course_materials': course_materials}
    else:
        course = Course.objects.get(pk=course_id)
        try:
            enroll = Enroll.objects.get(course=course, student=profile)
        except:
            enroll = None
        if enroll:
            enrolled = True
            completion = enroll.completed
        else:
            enrolled = False
            completion = False
        course_materials = CourseMaterial.objects.filter(course=course)
        first_material = course_materials.first()
        total_lessons = course_materials.count()
        context = {'user':user, 'course': course, 'profile': profile, 'course_materials': course_materials, 'enrolled': enrolled, 'total_lessons': total_lessons, 'first_material': first_material, 'completion': completion}

    return render(request, 'elearn_app/view_course.html', context)


def edit_course(request, user_id, course_id):
    user = User.objects.get(pk=user_id)
    course = Course.objects.get(pk=course_id)
    profile = Profile.objects.get(user=user)
    form = AddCourseForm()
    context = {'user': user, 'course': course, 'profile': profile, 'form': form}
    return render(request, 'elearn_app/edit_course.html', context)


@login_required
def delete_course(request, user_id, course_id):
    course = Course.objects.get(pk=course_id)
    user = User.objects.get(pk=user_id)
    course_name = course.name
    course.delete()
    messages.success(request, f'Course {course_name} has been deleted!')
    return redirect('home', user_id=user.pk, category='all')


def add_course_material(request, user_id, course_id):
    if request.method == "POST":
        form = AddCourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            file = form.cleaned_data.get('file')
            file_name = file.name # type: ignore
            user = User.objects.get(pk=user_id)
            course = Course.objects.get(pk=course_id)
            file.name = custom_filename(file.name) # type: ignore
            uploaded_at = timezone.now()
            course_material = CourseMaterial.objects.create(name=name, description=description, file=file, uploaded_at=uploaded_at, course=course)
            messages.success(request, f'Material {file_name} has been added to {course.name}')
            return redirect('home', user_id=user.pk, category='all')
    else:
        user = User.objects.get(pk=user_id)
        course = Course.objects.get(pk=course_id)
        profile = Profile.objects.get(user=user)
        form = AddCourseMaterialForm()
        context = {'user': user, 'profile': profile, 'course': course, 'form': form}
        return render(request, 'elearn_app/add_material.html', context)
    

def home_guest(request):
    return HttpResponse('You can view courses here!')


def all_courses(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    if profile.user_type == 'teacher':
        courses = Course.objects.filter(profile=profile)
        num_courses = courses.count()
        context = {'user': user, 'profile': profile, 'courses': courses, 'num_courses': num_courses}
        return render(request, 'elearn_app/all_courses.html', context)
    elif profile.user_type == 'student':
        enrolled_courses = Enroll.objects.filter(student=profile)
        context = {'user': user, 'profile': profile, 'courses': enrolled_courses}
        return render(request, 'elearn_app/all_courses.html', context)
    

def enroll_course(request, user_id, course_id):
    student_user = User.objects.get(pk=user_id)
    student = Profile.objects.get(user=student_user)
    course = Course.objects.get(pk=course_id)
    course_materials = CourseMaterial.objects.filter(course=course)
    teacher = course.profile
    enrolled_at = timezone.now()
    enroll = Enroll.objects.create(name=course.name, enrolled_at=enrolled_at, course=course, student=student, teacher=teacher)
    for material in course_materials:
        course_progress = CourseCompletionProgress.objects.create(course_material=material, student=student)
        course_progress.save()
    messages.success(request, f'You have enrolled in the course {course.name} by {teacher.user.username}')
    return redirect('home', user_id=student_user.pk, category='all')


def learn_course(request, user_id, course_id, course_material_id=1):
    course = Course.objects.get(pk=course_id)
    course_materials = CourseMaterial.objects.filter(course=course)
    current_material = CourseMaterial.objects.get(pk=course_material_id)
    next_material = course_materials.filter(pk__gt=course_material_id).first()
    has_next_material = True if next_material else False
    context = {'course': course, 'course_materials': course_materials, 'current_material': current_material, 'next_material': next_material, 'has_next': has_next_material}
    return render(request, 'elearn_app/enrolled_course_view.html', context)


def search_category(request, user_id):
    if request.method == 'POST':
        category = request.POST.get('category')
        category = category.capitalize()
        courses = Course.objects.filter(category=category)
        if courses.count() == 0:
            messages.error(request, f'No courses found for {category}! You can view other courses below.')
            return redirect('home', user_id=user_id, category='all')
        else:
            count = courses.count()
            user = User.objects.get(pk=user_id)
            context = {'user': user, 'courses': courses}
            messages.success(request, f'You have searched for {category}. We found {count} courses!')
            return redirect('home', user_id=user.pk, category=category)
    else:
        user = User.objects.get(pk=user_id)
        return redirect('home', user_id=user.pk, category='all')
    

def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    if profile.user_type == 'teacher':
        courses = Course.objects.filter(profile=profile)
        enrolls = Enroll.objects.filter(teacher=profile)
        # making a dictionary to store the number of enrollemnts in a certain course by the teacher
        if enrolls:   
            enrollment_count = {}
            for enroll in enrolls:
                if enroll.course_id not in enrollment_count: # type: ignore
                    enrollment_count[enroll.course_id] = 1 # type: ignore
                elif enroll.course_id in enrollment_count: # type: ignore
                    enrollment_count[enroll.course_id] += 1 # type: ignore
            # getting the course that has highest number of enrollments
            most_enrolled_course_id = max(enrollment_count, key=enrollment_count.get) #type: ignore
            # extracting the most enrolled course from database
            most_enrolled_course = Course.objects.get(pk=most_enrolled_course_id)
            context = {'user': user, 'profile': profile, 'courses': courses, 'most_enrolled_course': most_enrolled_course, 'students': enrolls}
            return render(request, 'elearn_app/profile.html', context)
        else:
            enrolls = 0
            most_enrolled_course = None
            context = {'user': user, 'profile': profile, 'courses': courses, 'most_enrolled_course': most_enrolled_course, 'students': enrolls}
            return render(request, 'elearn_app/profile.html', context)
    elif profile.user_type == 'student':
        enrolled_courses = Enroll.objects.filter(student=profile)
        context = {'user': user, 'profile': profile, 'courses': enrolled_courses}
        return render(request, 'elearn_app/profile.html', context)
    

def rate_course(request, user_id, course_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        rating = int(rating)
        course = Course.objects.get(pk=course_id)
        rated_at = timezone.now()
        user = User.objects.get(pk=user_id)
        student = Profile.objects.get(user=user)
        rate = Rating.objects.create(rating=rating, rated_at=rated_at, course=course, student=student)
        rate.save()
        messages.success(request, f'Your rating has been submitted for course {course.name}.')
        return redirect('home', user_id=user.pk, category='all')
    else:
        user = User.objects.get(pk=user_id)
        course = Course.objects.get(pk=course_id)
        profile = Profile.objects.get(user=user)
        try:
            enroll = Enroll.objects.get(student=profile, course=course)
        except: 
            enroll = None
        if enroll:      
            if enroll.completed:
                context = {'user': user, 'course': course, 'profile': profile}
                return render(request, 'elearn_app/rate_course.html', context)
            else:
                messages.error(request, 'You have not completed the course yet!')
                return redirect('home', user_id=user.pk, category='all')
        else:
            messages.error(request, 'You are not enrolled in this course yet.')
            return redirect('home', user_id=user.pk, category='all')
    

def course_completion(request, user_id, course_id):
    user = User.objects.get(pk=user_id)
    course = Course.objects.get(pk=course_id)
    profile = Profile.objects.get(user=user)
    enroll = Enroll.objects.get(student=profile, course=course)
    enroll.completed = True
    enroll.save()
    messages.success(request, f'Congratulations! You have completed the course {course.name}')
    return redirect('home', user_id=user.pk, category='all')


def complete_material(request, user_id, course_material_id, course_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    course = Course.objects.get(pk=course_id)
    course_material = CourseMaterial.objects.get(pk=course_material_id)
    course_material_completion = CourseCompletionProgress.objects.get(student=profile, course_material=course_material)
    course_material_completion.completed = True
    course_material_completion.completed_at = timezone.now()
    course_material_completion.save()
    messages.success(request, f'You have completed the lesson {course_material.name}')
    return redirect('learn', user_id=user.pk, course_id=course.pk, course_material_id=course_material.pk)

def edit_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = ChangeProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            file = data.get('user_image')
            file.name = custom_filename(file.name) #type: ignore
            profile.user_image = file # type: ignore
            profile.save()
            print(profile.user_image)
            messages.success(request, 'You profile picture has been updated!')
            return redirect('profile', user_id=user.pk)
        else:
            return HttpResponse('Form is not valid')
    else:
        form = ChangeProfilePictureForm()
        context = {'form': form, 'user': user, 'profile': profile}
        return render(request, 'elearn_app/edit_profile_image.html', context)

# function to give the user uploaded images and files a custom name as filename_randomStringSequence.extension
def custom_filename(filename):
    extension = filename.split('.')[-1]
    string_sequence = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 15)) 
    new_filename = f'{filename.split('.')[0]}_{string_sequence}.{extension}'
    return new_filename

