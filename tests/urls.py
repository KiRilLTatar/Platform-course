from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('module/<int:module_id>/add_test', views.add_test, name="add_test"),  
    path('test/<int:test_id>/add_question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/add_answer/', views.add_answer_option, name='add_answer_option'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('answer/<int:answer_id>/edit/', views.edit_answer_option, name='edit_answer_option'),
    path('answer/<int:answer_id>/delete/', views.delete_answer_option, name='delete_answer_option'),
    path('test/<int:test_id>/edit/', views.edit_test, name='edit_test'),
    path('test/<int:test_id>/delete/', views.delete_test, name='delete_test'),

]
