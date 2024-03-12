import logging
import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from nutrition.models import DailyMetabolism
from .models import UserProfile

logger = logging.getLogger(__name__)

# View for handling user login requests
class LoginView(APIView):
    # Handles GET request for login page
    def get(self, request):
        if request.user.is_authenticated:
            # Redirect to dashboard if user is already authenticated
            return redirect('dashboard')
        else:
            # Generate random string for client-side usage
            letters = string.digits
            q = ''.join(random.choice(letters) for i in range(10))
            return render(request, 'login.html', {'q': q})

    # Handles POST request for user login
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        # If authentication is successful, login the user
        if user:
            login(request, user)
            next_page = reverse('dashboard')
            return Response({'next_page': next_page}, status=status.HTTP_200_OK)
        else:
            # Log error based on whether the user exists
            user_exists = User.objects.filter(username=username).exists()
            error_message = "User exists, but authentication failed." if user_exists else "User does not exist."
            logger.error(error_message)
            # Respond with appropriate error message
            error_response = 'incorrect password' if user_exists else 'user not exist'
            return Response({'error': error_response}, status=status.HTTP_404_NOT_FOUND)

# View for handling user sign out
class SignOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

# View for handling user sign up requests
class SignupView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'next_page': reverse('dashboard')})
        return render(request, 'signup.html')

    def post(self, request, *args, **kwargs):
        username, email, password = request.data.get('username'), request.data.get('email'), request.data.get('password')

        if not all([username, email, password]):
            return Response({'message': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=username, email=email, password=make_password(password))
        login(request, user) # Auto-login after sign up
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

# View for checking if username or email already exists
class SignupCheckView(APIView):
    def get(self, request):
        username, email = request.GET.get('username'), request.GET.get('email')
        response_data = {}

        if username:
            response_data['exists'] = User.objects.filter(username=username).exists()
        elif email:
            response_data['exists'] = User.objects.filter(email=email).exists()
        else:
            return Response({'exists': False}, status=status.HTTP_200_OK)

        return Response(response_data, status=status.HTTP_200_OK)

# View for handling user profile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        profile_complete = all([profile, profile.gender, profile.age, profile.height, profile.weight])

        return render(request, 'profile.html', {
            'username': user.username,
            'email': user.email,
            'profile_complete': profile_complete,
            'profile': profile
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.age, profile.gender, profile.height, profile.weight = \
            request.data.get('age', profile.age), request.data.get('gender', profile.gender), \
            request.data.get('height', profile.height), request.data.get('weight', profile.weight)

        profile.save()
        # BMR calculation
        bmr_formula = 88.362 + (13.397 * profile.weight) + (4.799 * profile.height) - (5.677 * profile.age) \
            if profile.gender == 'male' \
            else 447.593 + (9.247 * profile.weight) + (3.098 * profile.height) - (4.330 * profile.age)

        daily_metabolism, _ = DailyMetabolism.objects.get_or_create(
            user=user, 
            date=timezone.now().date(), 
            defaults={'bmr': bmr_formula, 'intake': 0, 'exercise_metabolism': 0, 'total': bmr_formula}
        )
        daily_metabolism.bmr, daily_metabolism.total = bmr_formula, daily_metabolism.intake - bmr_formula - daily_metabolism.exercise_metabolism
        daily_metabolism.save()

        return Response({'message': 'Profile updated successfully', 'bmr': bmr_formula}, status=status.HTTP_200_OK)
