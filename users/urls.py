from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('check-username/', views.check_username, name='check_username'),
    path('profile/info/', views.profile_info, name='profile_info'),
    path('profile/course/', views.profile_course, name='profile_course'),
    path('profile/later/', views.profile_later_course, name='profile_later'),
    path('profile/statistic/', views.profile_statistic, name='profile_statistic')
]
