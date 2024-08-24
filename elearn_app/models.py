from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    user_image = models.ImageField(upload_to='profile_pics', blank=True, default='default.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
