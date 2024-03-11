# UserProfile/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('sign_out/', views.LoginView.as_view(), name='signout'),
    path('check_username_email/', views.check_username_email),
]
