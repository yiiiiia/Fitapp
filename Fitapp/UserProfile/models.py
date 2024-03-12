import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    A model representing additional information about a user.

    Attributes:
        user: A one-to-one relationship with Django's built-in User model.
        age: An optional positive integer field for the user's age.
        gender: A choice field for the user's gender with options 'male', 'female', and 'other'.
        height: An optional float field for the user's height.
        weight: An optional float field for the user's weight.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='Age')
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other', verbose_name='Gender')
    height = models.FloatField(null=True, blank=True, verbose_name='Height')
    weight = models.FloatField(null=True, blank=True, verbose_name='Weight')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    A signal receiver that creates or updates the UserProfile instance associated with a User instance.

    This receiver function is triggered every time a User instance is saved. It checks if a new User instance was created
    (indicated by the 'created' parameter). If a new User instance is created, it also creates a new UserProfile instance
    and associates it with the User instance. If the User instance already exists, it saves the associated UserProfile instance.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
