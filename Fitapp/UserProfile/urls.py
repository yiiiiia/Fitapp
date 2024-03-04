# UserProfile/urls.py
from django.urls import path
from . import views
from .views import LoginView, SignupView, UserProfileUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile', UserProfileUpdateView.as_view(), name='profile-update'),
    path('update_profile/', views.update_profile, name='update_profile'),
]
