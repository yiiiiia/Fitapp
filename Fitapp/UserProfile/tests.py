from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import UserProfile

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
