from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('food_page/', views.food_page, name='food_page'),
    path('add_exercise/', views.add_exercise, name='add_exercise'),
]
