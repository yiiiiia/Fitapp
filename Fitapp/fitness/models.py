from django.db import models
from django.conf import settings

class ExerciseBook(models.Model):
    exercise_name = models.CharField(max_length=30)
    calories_burned_per_min = models.FloatField()
    image = models.ImageField(upload_to='exercise_images/')

    def __str__(self):
        return f"{self.exercise_name}"

class ExerciseDone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey('ExerciseBook', on_delete=models.CASCADE)
    duration = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.exercise} - {self.duration} mins"
