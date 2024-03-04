from django.db import models
from django.conf import settings

class ExerciseBook(models.Model):
    exercise_name = models.CharField(max_length=30)
    calories_burned_per_min = models.FloatField()

    def __str__(self):
        return f"{self.exercise_name}"
