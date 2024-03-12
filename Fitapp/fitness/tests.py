from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from .models import ExerciseBook, ExerciseDone
from nutrition.models import DailyMetabolism
import json

class FitnessAppTestCase(TestCase):
    """
    Test case for the Fitness app.
    This includes testing for exercise models, views, and their interactions with the DailyMetabolism model.
    """

    def setUp(self):
        """
        Set up the initial data for the test case.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

        # Create test exercise
        self.exercise = ExerciseBook.objects.create(
            exercise_name='Running',
            calories_burned_per_min=10
        )

    def test_exercise_creation(self):
        """
        Test the creation of an exercise instance.
        """
        self.assertEqual(ExerciseBook.objects.count(), 1)
        self.assertEqual(ExerciseBook.objects.get(id=self.exercise.id).exercise_name, 'Running')

    def test_add_exercise_done(self):
        """
        Test the addition of an exercise done record.
        """
        data = {
            'exercise': self.exercise.id,
            'duration': 30,  # 30 minutes
            'date': str(timezone.now().date())
        }
        response = self.client.post(reverse('add_exercise_done'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exercise_done_affects_metabolism(self):
        """
        Test if recording an exercise done affects the DailyMetabolism record correctly.
        """
        data = {
            'exercise': self.exercise.id,
            'duration': 30,  # 30 minutes
            'date': str(timezone.now().date())
        }
        self.client.post(reverse('add_exercise_done'), data, content_type='application/json')
        daily_metabolism = DailyMetabolism.objects.get(user=self.user, date=timezone.now().date())
        expected_calories_burned = 30 * 10  # 30 minutes * 10 calories per minute
        self.assertEqual(daily_metabolism.exercise_metabolism, expected_calories_burned)
