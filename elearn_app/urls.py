from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/<int:user_id>/', views.home, name='home'),
    path('add/<int:user_id>/', views.add_course, name='add'), 
    path('view/<int:user_id>/<int:course_id>/', views.view_course, name='view'),
    path('courses/<int:user_id>/', views.all_courses, name='courses'),
    path('delete/<int:user_id>/<int:course_id>/', views.delete_course, name='delete'),
    path('edit/<int:user_id>/<int:course_id>/', views.edit_course, name='edit'),
    path('add_material/<int:user_id>/<int:course_id>/', views.add_course_material, name='add_material'),
    path('guest_home/', views.home_guest, name='guest_home'),
]