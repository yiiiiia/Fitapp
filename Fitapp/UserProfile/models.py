from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    age = models.PositiveIntegerField(null=True, verbose_name='Age')
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')], verbose_name='Gender')
    height = models.FloatField(null=True, verbose_name='Height')
    weight = models.FloatField(null=True, verbose_name='Weight')

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)