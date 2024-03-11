# UserProfile/urls.py
from django.urls import path, re_path

from . import views
from .views import LoginView, SignupView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('sign_out/', LoginView.as_view(), name='signout'),
    path('check_username_email/', views.check_username_email),
]
