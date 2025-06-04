from django.urls import path
from . import views
import tests.views as tests 

app_name = 'courses'

urlpatterns = [
     path('', views.course_list, name="course_list"),
     path('create_course/', views.create_course, name="create_course"),
     path('manage_course/', views.manage_course, name='manage_course'),
     path('<int:course_id>/', views.course_detail, name='course_detail'),
     path('<int:course_id>/course_progress/', views.course_detail_progress, name='course_progress'),
     path('<int:course_id>/edit_course/', views.edit_course, name='edit_course'),
     path('<int:course_id>/add_module/', views.add_module, name='add_module'),
     path('<int:course_id>/enroll/', views.add_course, name='add_course'),
     path('<int:course_id>/remove/', views.remove_course, name='remove_course'), # удаление из списка прохождения
     path('<int:course_id>/delete/', views.delete_course, name='delete_course'), # удаление курса в целом
     path('<int:module_id>/add_lesson/', views.add_lesson, name='add_lesson'),
     path('<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'), 
     path('<int:lesson_id>/lesson_progress/', views.lesson_detail_progress, name='lesson_progress'),
     path('module/<int:module_id>/delete/', views.delete_module, name='delete_module'),
     path('lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
     path('material/<int:material_id>/delete/', views.delete_material, name='delete_material'),
]
