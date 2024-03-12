from django.db import models
from django.conf import settings
from nutrition.models import DailyMetabolism

class ExerciseBook(models.Model):
    exercise_name = models.CharField(max_length=30)
    calories_burned_per_min = models.FloatField()
    image = models.ImageField(upload_to='exercise_images/')

    def __str__(self):
        # String representation of the exercise.
        return f"{self.exercise_name}"

class ExerciseDone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey('ExerciseBook', on_delete=models.CASCADE)
    duration = models.IntegerField()# Duration of exercise in minutes
    date = models.DateField()

    def save(self, *args, **kwargs):
        # Logic executed before saving
        super().save(*args, **kwargs)  # Call the save method of the parent class

        # Calculating calories burned
        calories_burned = self.exercise.calories_burned_per_min * self.duration

        # Get or create a DailyMetabolism record for the current day.
        daily_metabolism, created = DailyMetabolism.objects.get_or_create(
            user=self.user,
            date=self.date,
            defaults={'bmr': 0, 'intake': 0, 'exercise_metabolism': 0, 'total': 0}
        )

        # Update Exercise_Metabolism and Total
        daily_metabolism.exercise_metabolism += calories_burned
        daily_metabolism.total = daily_metabolism.intake - daily_metabolism.bmr - daily_metabolism.exercise_metabolism
        daily_metabolism.save()

    def __str__(self):
        # String representation of the exercise done.
        return f"{self.exercise} - {self.duration} mins"
