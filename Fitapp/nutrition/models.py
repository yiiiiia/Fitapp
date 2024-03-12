from django.db import models
from django.conf import settings

class FoodEaten(models.Model):
    """
    Represents a record of food consumed by a user.

    - user: The user who ate the food.
    - food: The type of food eaten.
    - amount: The amount of food consumed.
    - date: The date when the food was eaten.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey('FoodBook', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()

    def save(self, *args, **kwargs):
        # First save the FoodEaten object normally
        super().save(*args, **kwargs)

        # Calculate the calories in this food intake
        calories_consumed = self.food.calories_per_gram * self.amount

        # Get or create a DailyMetabolism object for the corresponding date.
        daily_metabolism, created = DailyMetabolism.objects.get_or_create(
            user=self.user,
            date=self.date,
            defaults={'bmr': 0, 'intake': 0, 'exercise_metabolism': 0, 'total': 0}
        )

        # Updating the intake and total fields of the DailyMetabolism object
        if not created:
            daily_metabolism.intake += calories_consumed
        else:
            daily_metabolism.intake = calories_consumed

        # Recalculating the total field
        daily_metabolism.total = daily_metabolism.intake - daily_metabolism.bmr - daily_metabolism.exercise_metabolism

        # Save the DailyMetabolism object
        daily_metabolism.save()

    def __str__(self):
        return f"{self.food} - {self.amount}"

class DailyMetabolism(models.Model):
    """
    Keeps track of a user's daily metabolism data.

    - user: The user this metabolism data belongs to.
    - date: The date for the metabolism data.
    - bmr: Basal Metabolic Rate.
    - intake: Total calorie intake.
    - exercise_metabolism: Calories burned through exercise.
    - total: Net calories after accounting for intake and exercise.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    bmr = models.FloatField()
    intake = models.FloatField()
    exercise_metabolism = models.FloatField()
    total = models.FloatField()

    def save(self, *args, **kwargs):
        # Round floating point numbers before saving to database
        self.bmr = round(self.bmr, 1)
        self.intake = round(self.intake, 1)
        self.exercise_metabolism = round(self.exercise_metabolism, 1)
        self.total = round(self.total, 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"BMR: {self.bmr}, Total: {self.total}"

class FoodBook(models.Model):
    """
    Represents a food item in the food database.

    - food_type: The category of the food.
    - food_name: The name of the food item.
    - image: An image representing the food.
    - calories_per_gram: Calories per gram of the food.
    - protein_per_gram: Protein content per gram.
    - fat_per_gram: Fat content per gram.
    - carbohydrate_per_gram: Carbohydrates per gram.
    - other_per_gram: Other nutrients per gram.
    """
    food_type = models.CharField(max_length=30)
    food_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='food_images/')
    calories_per_gram = models.FloatField()
    protein_per_gram = models.FloatField()
    fat_per_gram = models.FloatField()
    carbohydrate_per_gram = models.FloatField()
    other_per_gram = models.FloatField()

    def __str__(self):
        return self.food_name
