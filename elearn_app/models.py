from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    user_image = models.ImageField(upload_to='profile_pics', blank=True, default='profile_pics/default.png', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(editable=False)
    image = models.ImageField(upload_to='course_pics', blank=True, default='course_pics/default.jpg', null=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class CourseMaterial(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    file = models.FileField(upload_to='course_materials', null=False)
    uploaded_at = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
