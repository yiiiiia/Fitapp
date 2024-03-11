import random
import string

from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .forms import ExerciseBookForm


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'dashboard.html', {'username': request.user.get_username()})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_exercise(request):
    if request.method == 'POST':
        # DRF方式处理表单数据
        # ... 逻辑 ...
        form = ExerciseBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_view_name')
        # 如果表单无效，继续显示表单及错误信息
    else:
        form = ExerciseBookForm()

    return render(request, 'add_exercise.html', {'form': form})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exercise_page(request):
    return render(request, 'food_exercise.html')
