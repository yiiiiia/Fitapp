# views.py
import logging
from urllib import request

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile

logger = logging.getLogger(__name__)


def set_user_in_session(request, user):
    request.session['user_id'] = user.id
    request.session.set_expiry(24 * 3600)


def login_required(func):
    def wrapper(request):
        if request.session.get('user_id'):
            return func(request)
        else:
            return redirect('login')
    return wrapper


class LoginView(APIView):
    def get(self, request):
        if request.session.get('user_id'):
            return redirect('dashboard')
        else:
            return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            set_user_in_session(request, user)
            next_page = reverse('dashboard')
            return JsonResponse({'next_page': next_page}, status=200)
        else:
            if User.objects.filter(username=username).exists():
                logger.error("User exists, but authentication failed.")
                return JsonResponse({'error': 'incorrect password'}, status=404)
            else:
                logger.error("User does not exist.")
                return JsonResponse({'error': 'user not exist'}, status=404)


class SignupView(APIView):
    def get(self, request):
        if request.session.get('user_id'):
            return redirect('dashboard')
        else:
            loginURL = reverse('login')
            return render(request, 'signup.html', {'login_page': loginURL})

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not (username and email and password):
            return JsonResponse({'message': 'Missing fields'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already in use'}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # 密码加密
        )
        user.save()
        return JsonResponse({'message': 'User created successfully'}, status=201)


# implement for font-end validation
def check_username_email(request):
    username = request.GET.get('username')
    email = request.GET.get('email')
    if username:
        if User.objects.filter(username=username).exists():
            return JsonResponse({'exists': True}, status=200)
        else:
            return JsonResponse({'exists': False}, status=200)
    elif email:
        if User.objects.filter(email=email).exists():
            return JsonResponse({'exists': True}, status=200)
        else:
            return JsonResponse({'exists': False}, status=200)
    else:
        return JsonResponse({'error': 'invalid parameter'}, status=400)


def update_profile(request):
    return render(request, 'update_profile.html')


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user)
        user_profile.gender = request.data.get('gender')
        user_profile.age = request.data.get('age')
        user_profile.height = request.data.get('height')
        user_profile.weight = request.data.get('weight')
        logger.error(user_profile.user)
        user_profile.save()

        return Response({'message': 'Profile updated successfully'}, status=200)
