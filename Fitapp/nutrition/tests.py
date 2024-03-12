from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import FoodBook, FoodEaten, DailyMetabolism
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
import json

class NutritionAppTestCase(TestCase):
    """
    Test case for the Nutrition app.

    This test case covers the creation and retrieval of food items and food eaten records,
    along with the computation of daily metabolism data.
    """

    def setUp(self):
        """
        Set up the initial data for the test case.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create test food items
        self.food1 = FoodBook.objects.create(
            food_type='Fruit',
            food_name='Apple',
            calories_per_gram=0.52,
            protein_per_gram=0.03,
            fat_per_gram=0.02,
            carbohydrate_per_gram=0.14,
            other_per_gram=0.01
        )

        self.food2 = FoodBook.objects.create(
            food_type='Vegetable',
            food_name='Carrot',
            calories_per_gram=0.41,
            protein_per_gram=0.01,
            fat_per_gram=0.01,
            carbohydrate_per_gram=0.10,
            other_per_gram=0.01
        )

        # Create a DailyMetabolism record
        self.daily_metabolism = DailyMetabolism.objects.create(
            user=self.user,
            date=timezone.now().date(),
            bmr=0,
            intake=0,
            exercise_metabolism=0,
            total=0
        )

    def test_food_eaten_creation_and_total_intake(self):
        """
        Test the creation of FoodEaten records and calculate total calorie intake.
        """
        # Add food eaten records
        FoodEaten.objects.create(user=self.user, food=self.food1, amount=100, date=timezone.now().date()) # 100 grams of Apple
        FoodEaten.objects.create(user=self.user, food=self.food2, amount=150, date=timezone.now().date()) # 150 grams of Carrot

        # Fetch the DailyMetabolism record for today
        daily_metabolism = DailyMetabolism.objects.get(user=self.user, date=timezone.now().date())

        # Verify the total calorie intake
        expected_total_intake = (self.food1.calories_per_gram * 100) + (self.food2.calories_per_gram * 150)
        self.assertAlmostEqual(daily_metabolism.intake, expected_total_intake, places=1,
                               msg="Total calorie intake does not match expected value.")

class NutritionViewsTestCase(TestCase):
    """
    Test case for the views in the Nutrition app.
    This includes tests for listing food items, adding food consumed, and retrieving user-related data.
    """

    def setUp(self):
        """
        Set up the initial data for the test case.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

        # Create test food items
        self.food1 = FoodBook.objects.create(
            food_type='Fruit',
            food_name='Apple',
            calories_per_gram=0.52,
            protein_per_gram=0.03,
            fat_per_gram=0.02,
            carbohydrate_per_gram=0.14,
            other_per_gram=0.01
        )

        # Create a DailyMetabolism record
        self.daily_metabolism = DailyMetabolism.objects.create(
            user=self.user,
            date=timezone.now().date(),
            bmr=0,
            intake=0,
            exercise_metabolism=0,
            total=0
        )

    def test_food_list_view(self):
        """
        Test retrieving the list of food items.
        """
        response = self.client.get(reverse('food_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Apple', response.content.decode())

    def test_add_food_eaten_view(self):
        """
        Test adding a food item to the user's food eaten list.
        """
        data = {
            'food': self.food1.id,
            'amount': 100,  # 100 grams
            'date': str(timezone.now().date())
        }
        response = self.client.post(reverse('add_food_eaten'), data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FoodEaten.objects.count(), 1)

    def test_user_related_data_view(self):
        """
        Test retrieving food eaten by the user and their daily metabolism data.
        """
        response = self.client.get(reverse('user_related_data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)