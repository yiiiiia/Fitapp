import logging
import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from nutrition.models import DailyMetabolism
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile

logger = logging.getLogger(__name__)


class LoginView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            letters = string.digits
            q = ''.join(random.choice(letters) for i in range(10))
            return render(request, 'login.html', {'q': q})

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


class SignOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


class SignupView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            next_page = reverse('dashboard')
            return Response({'next_page': next_page})
        else:
            return render(request, 'signup.html')

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


class SignupCheckView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        email = request.GET.get('email')
        if username:
            if User.objects.filter(username=username).exists():
                return Response({'exists': True}, status=status.HTTP_200_OK)
            else:
                return Response({'exists': False}, status=status.HTTP_200_OK)
        elif email:
            if User.objects.filter(email=email).exists():
                return Response({'exists': True}, status=status.HTTP_200_OK)
            else:
                return Response({'exists': False}, status=status.HTTP_200_OK)
        else:
            return Response({'exists': False}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user_id=user.id)
        if profile:
            if profile.gender:
                profile.gender = profile.gender.title()
            if profile.height:
                profile.height = '{:.1f}'.format(profile.height)
            if profile.weight:
                profile.weight = '{:.1f}'.format(profile.weight)
        return render(request, 'profile.html', {'username': user.get_username(), 'email': user.email, 'profile': profile})

    def post(self, request, *args, **kwargs):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        profile.age = request.data.get('age', profile.age)
        profile.gender = request.data.get('gender', profile.gender)
        profile.height = request.data.get('height', profile.height)
        profile.weight = request.data.get('weight', profile.weight)
        profile.save()

        # 计算 BMR
        if profile.gender == 'male':
            bmr = 88.362 + (13.397 * profile.weight) + (4.799 *
                                                        profile.height) - (5.677 * profile.age)
        else:
            bmr = 447.593 + (9.247 * profile.weight) + (3.098 *
                                                        profile.height) - (4.330 * profile.age)

        # 更新 DailyMetabolism
        daily_metabolism, created = DailyMetabolism.objects.get_or_create(user=user, date=timezone.now().date(), defaults={
            'bmr': bmr, 'intake': 0, 'exercise_metabolism': 0, 'total': bmr
        })
        daily_metabolism.bmr = bmr
        daily_metabolism.total = daily_metabolism.intake - \
            bmr - daily_metabolism.exercise_metabolism
        daily_metabolism.save()

        return Response({'message': 'Profile updated successfully', 'bmr': bmr}, status=status.HTTP_200_OK)
