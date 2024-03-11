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
from .models import ExerciseBook
from rest_framework.response import Response


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