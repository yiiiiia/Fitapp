from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    path('exercise_page/', views.exercise_page, name='exercise_page'),
    path('add_exercise_done/', views.AddExerciseDoneView.as_view(), name='add-exercise-done'),
]
