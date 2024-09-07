from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/<int:user_id>/<str:category>/', views.home, name='home'),
    path('add/<int:user_id>/', views.add_course, name='add'), 
    path('view/<int:user_id>/<int:course_id>/', views.view_course, name='view'),
    path('courses/<int:user_id>/', views.all_courses, name='courses'), #type: ignore
    path('delete/<int:user_id>/<int:course_id>/', views.delete_course, name='delete'),
    path('edit/<int:user_id>/<int:course_id>/', views.edit_course, name='edit'),
    path('add_material/<int:user_id>/<int:course_id>/', views.add_course_material, name='add_material'), #type: ignore
    path('enroll/<int:user_id>/<int:course_id>/', views.enroll_course, name='enroll'),
    path('learn-course/<int:user_id>/<int:course_id>/<int:course_material_id>/', views.learn_course, name='learn'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'), #type: ignore
    path('search/<int:user_id>/', views.search_category, name='search'),
    path('guest_home/', views.home_guest, name='guest_home'),
    path('rate-course/<int:user_id>/<int:course_id>/', views.rate_course, name='rate'),
    path('course-completion/<int:user_id>/<int:course_id>/', views.course_completion, name='complete'),
    path('coursematerial-completion/<int:user_id>/<int:course_material_id>/<int:course_id>/', views.complete_material, name='complete_material'),
    path('edit-profile/<int:user_id>/', views.edit_profile, name='edit-profile')
]