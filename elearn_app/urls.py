from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/<int:user_id>/', views.home, name='home'),
    path('add/<int:user_id>/', views.add_course, name='add'), 
]