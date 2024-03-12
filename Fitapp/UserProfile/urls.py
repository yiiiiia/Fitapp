# UserProfile/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('signout/', views.SignOutView.as_view(), name='signout'),
    path('signup_check/', views.SignupCheckView.as_view(), name='signup_check'),
]

