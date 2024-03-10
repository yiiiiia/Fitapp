from django.urls import path

from . import views

urlpatterns = [
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    path('exercise_page/', views.exercise_page, name='exercise_page'),
]
