from django.db import models
from django.conf import settings

class FoodEaten(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey('FoodBook', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.food} - {self.amount}"

class DailyMetabolism(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    bmr = models.FloatField()
    intake = models.FloatField()
    exercise_metabolism = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"BMR: {self.bmr}, Total: {self.total}"

class FoodBook(models.Model):
    food_type = models.CharField(max_length=30)
    food_name = models.CharField(max_length=100)
    calories_per_gram = models.FloatField()
    protein_per_gram = models.FloatField()
    fat_per_gram = models.FloatField()
    carbohydrate_per_gram = models.FloatField()
    other_per_gram = models.FloatField()

    def __str__(self):
        return self.food_name
