# views.py
import logging

from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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


def login_required(func):
    def wrapper(request):
        if request.session.get('user_id'):
            return func(request)
        else:
            return redirect('login')
    return wrapper


def sign_out(request):
    if request.session.get('user_id'):
        del request.session['user_id']
    return redirect('login')


class LoginView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # 使用Django的login函数来处理登录
            next_page = reverse('dashboard')
            return Response({'next_page': next_page}, status=status.HTTP_200_OK)
        else:
            if User.objects.filter(username=username).exists():
                logger.error("User exists, but authentication failed.")
                return Response({'error': 'incorrect password'}, status=status.HTTP_404_NOT_FOUND)
            else:
                logger.error("User does not exist.")
                return Response({'error': 'user not exist'}, status=status.HTTP_404_NOT_FOUND)


class SignupView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            next_page = reverse('dashboard')
            return Response({'next_page': next_page})
        else:
            loginURL = reverse('login')
            return Response({'login_page': loginURL})

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not (username and email and password):
            return Response({'message': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # 密码加密
        )
        user.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return render(request, 'profile.html', {'username': user.get_username(), 'email': user.email})

    def post(self, request):
        return JsonResponse({'msg': 'good'}, status=200)

    def put(self, request):
        return JsonResponse({'msg': 'good'}, status=200)


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
