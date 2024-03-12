import logging
import random
import string

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ExerciseBookForm
from .models import ExerciseBook, ExerciseDone

logger = logging.getLogger(__name__)


class DashboardView(APIView):
    """
    View for rendering the dashboard page for authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'dashboard.html', {'username': request.user.get_username()})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_exercise(request):
    """
    View for adding a new exercise record.
    Handles both GET and POST requests.
    """
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
    """
    View for rendering the exercise page.
    Generates a random query parameter 'q' for each request.
    """
    q = ''.join(random.choice(string.digits) for _ in range(10))
    return render(request, 'food_exercise.html', {
        'food_page': False,
        'page_type': 'exercise',
        'q': q,
        'username': request.user.get_username()
    })


class ExerciseListView(APIView):
    """
    API view for listing exercises.
    Allows filtering based on a search query.
    """

    def get(self, request):
        search_query = request.query_params.get('search', None)
        if search_query:
            exercises = ExerciseBook.objects.filter(
                Q(exercise_name__icontains=search_query))
        else:
            exercises = ExerciseBook.objects.all()

        data = [
            {
                "id": exercise.id,
                "name": exercise.exercise_name,
                "calorie": exercise.calories_burned_per_min * 100,
                "image": request.build_absolute_uri(exercise.image.url) if exercise.image else None
            } for exercise in exercises
        ]
        return Response(data)


class AddExerciseDoneView(APIView):
    """
    API view for recording an exercise done by a user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            exercise_id = request.data.get('exercise')
            duration = request.data.get('duration')
            date = request.data.get('date') or timezone.now().date()

            exercise = ExerciseBook.objects.get(id=exercise_id)
            ExerciseDone.objects.create(
                user=user, exercise=exercise, duration=duration, date=date)

            return JsonResponse({'message': 'Exercise recorded successfully'})
        except ExerciseBook.DoesNotExist:
            logger.error(f"Exercise with ID {exercise_id} not found")
            return JsonResponse({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AddExerciseDoneView: {e}")
            raise APIException(f"An error occurred: {e}")
