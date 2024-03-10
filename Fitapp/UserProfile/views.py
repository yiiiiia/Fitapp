import random
import string

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.views import APIView


def login_required(func):
    def wrapper(request):
        if request.session.get('user_id'):
            return func(request)
        else:
            return redirect('login')
    return wrapper


@login_required
def sign_out(request):
    if request.session.get('user_id'):
        del request.session['user_id']
    return redirect('login')


class LoginView(APIView):
    def get(self, request):
        if request.session.get('user_id'):
            return redirect('dashboard')
        else:
            letters = string.digits
            q = ''.join(random.choice(letters) for i in range(10))
            return render(request, 'login.html', {'q': q})

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            request.session['user_id'] = user.id
            request.session.set_expiry(24 * 3600)
            next_page = reverse('dashboard')
            return JsonResponse({'next_page': next_page}, status=200)
        else:
            if not User.objects.filter(username=username).exists():
                return JsonResponse({'err_msg': 'user does not exist', 'err_code': 1}, status=404)
            else:
                return JsonResponse({'err_msg': 'incorrect password', 'err_code': 2}, status=404)


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


@login_required
def user_profile(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        return render(request, 'profile.html', {'username': user.get_username(), 'email': user.email})
    elif request.method == 'POST' or request.method == "PUT":
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
