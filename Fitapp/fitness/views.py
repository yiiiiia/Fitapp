import random
import string
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .forms import ExerciseBookForm
from .models import ExerciseBook, ExerciseDone
from nutrition.models import DailyMetabolism
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'dashboard.html', {'username': request.user.get_username()})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_view_name')
    else:
        form = ExerciseBookForm()

    return render(request, 'add_exercise.html', {'form': form})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exercise_page(request):
    return render(request, 'food_exercise.html')

class ExerciseListView(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', None)
        if search_query:
            exercises = ExerciseBook.objects.filter(
                Q(exercise_name__icontains=search_query)
            )
        else:
            exercises = ExerciseBook.objects.all()
        data = [
            {
                "id": exercise.id,
                "name": exercise.exercise_name,
                "calories_burned_per_min": exercise.calories_burned_per_min * 100,
                "image": request.build_absolute_uri(exercise.image.url) if exercise.image else None
            } for exercise in exercises
        ]
        return Response(data)
    
class AddExerciseDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        exercise_id = request.data.get('exercise')
        duration = request.data.get('duration')
        date = request.data.get('date') or timezone.now().date()

        exercise = ExerciseBook.objects.get(id=exercise_id)
        ExerciseDone.objects.create(user=user, exercise=exercise, duration=duration, date=date)

        # 检查是否已存在 DailyMetabolism 记录
        daily_metabolism, created = DailyMetabolism.objects.get_or_create(user=user, date=date, defaults={
            'bmr': 0, 'intake': 0, 'exercise_metabolism': 0, 'total': 0
        })

        # 更新 exercise_metabolism 和 total
        exercise_calories = exercise.calories_burned_per_min * duration
        daily_metabolism.exercise_metabolism += exercise_calories
        daily_metabolism.total = daily_metabolism.bmr + daily_metabolism.intake - daily_metabolism.exercise_metabolism
        daily_metabolism.save()

        return JsonResponse({'message': 'Exercise recorded successfully'})