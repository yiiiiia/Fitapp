# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import AuthToken
import logging

logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        logger.error(username)
        logger.error(password)
        user = authenticate(username=username, password=password)
        if user:
            # 创建或获取 token
            token, created = AuthToken.objects.get_or_create(user=user)
            response = Response()
            response.set_cookie(key='access_token', value=str(token.token), httponly=True)
            return response
        else:
            if User.objects.filter(username=username).exists():
                logger.error("User exists, but authentication failed.")
            else:
                logger.error("User does not exist.")
            return Response(status=404)
class SignupView(APIView):
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