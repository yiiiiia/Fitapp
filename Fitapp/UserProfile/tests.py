from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from nutrition.models import DailyMetabolism
from UserProfile.middleware import DailyMetabolismMiddleware
from .models import UserProfile
from django.utils import timezone

class UserModelTest(TestCase):
    """
    Test cases for the User and UserProfile models.
    """

    def setUp(self):
        """
        Set up method for user model tests.
        Creates a user instance before each test method.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_user_creation(self):
        """
        Test the creation of a user instance.
        Verifies whether the created user is an instance of the User model.
        Checks if the user is neither staff nor superuser by default.
        """
        self.assertTrue(isinstance(self.user, User))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_user_profile_creation(self):
        """
        Test automatic creation of UserProfile instance.
        Checks if the UserProfile instance is created and associated with the User instance.
        """
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertTrue(isinstance(user_profile, UserProfile))
        self.assertEqual(user_profile.user.username, 'testuser')

    def test_user_profile_str(self):
        """
        Test the string representation of the UserProfile instance.
        Verifies that the string representation matches the username of the associated user.
        """
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(user_profile), 'testuser')

class UserRegistrationAndLoginTest(TestCase):
    """
    Test cases for user registration and login processes.
    """

    def setUp(self):
        """
        Set up method for user registration and login tests.
        Initializes an APIClient instance before each test method.
        """
        self.client = APIClient()

    def test_user_registration(self):
        """
        Test the user registration endpoint.
        Verifies that a new user can be successfully registered and a 201 status code is returned.
        """
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'new_password'
        }
        response = self.client.post(reverse('signup'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        """
        Test the user login endpoint.
        Verifies that a user can log in with correct credentials and a 200 status code is returned.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DailyMetabolismMiddlewareTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Get the UserProfile instance, which will be created with the post_save signal.
        self.profile = UserProfile.objects.get(user=self.user)

        # Set the UserProfile field manually.
        self.profile.age = 25
        self.profile.gender = 'male'
        self.profile.height = 175
        self.profile.weight = 70
        self.profile.save()

    def test_daily_metabolism_update(self):
        # Creating a Middleware Instance
        middleware = DailyMetabolismMiddleware(lambda x: x)

        # Simulation Middleware Update DailyMetabolism
        middleware.update_daily_metabolism(self.user)

        # Get today's DailyMetabolism record!
        today = timezone.now().date()
        daily_metabolism = DailyMetabolism.objects.get(user=self.user, date=today)

        # Calculate the expected BMR value
        expected_bmr = 88.362 + (13.397 * self.profile.weight) + (4.799 * self.profile.height) - (5.677 * self.profile.age)

        # Assertion to check if BMR is up to date
        self.assertEqual(daily_metabolism.bmr, round(expected_bmr, 1))

    def tearDown(self):
        self.user.delete()
        self.profile.delete()