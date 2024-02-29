from django.db import models
from django.db.models.constraints import UniqueConstraint


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=30, unique=True)

    def __str__(self):
        return f'Id: {self.id}, Name: {self.first_name} {self.last_name},\
                Email: {self.email}, Password: ******'


class Administrator(models.Model):
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=30, unique=True)

    def __str__(self):
        return f'Id: {self.id}, Email: {self.email}, Password: ******'


class Profile(models.Model):
    gender = models.IntegerField()
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Id: {self.id}, Gender: {self.gender}, Age: {self.age},\
                Height: {self.height}, Weight: {self.weight},\
                User_id: {self.user}'


class DailyMetabolism(models.Model):
    date = models.DateField(auto_now_add=True, )
    # bmr depends on weight, user's weight can change, so this field defaults
    # to the 'weight' in table Profile
    daily_weight = models.FloatField()

    bmr = models.FloatField(default=.0)
    intake_calorie = models.FloatField(default=.0)
    exercise_calorie = models.FloatField(default=.0)
    total_calorie = models.FloatField(default=.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'date'], name='unique_user_date')
        ]

    def __str__(self):
        return f'Id: {self.id}, user_id: {self.user},\
                Date: {self.date}, Daily Weight: {self.daily_weight},\
                BMR: {self.bmr}, Intake Calorie: {self.intake_calorie},\
                Exercise burn calorie: {self.exercise_calorie}\
                Total calorie: {self.total_calorie}'


class FoodBook(models.Model):
    food_type = models.CharField(max_length=30, )
    food_name = models.CharField(max_length=100, unique=True)
    calories_per_gram = models.FloatField(default=.0, )
    fat_per_gram = models.FloatField(default=.0, )
    protein_per_gram = models.FloatField(default=.0, )
    carbohydrate_per_gram = models.FloatField(default=.0, )

    def __str__(self):
        return f'Id: {self.id}'


class ExerciseBook(models.Model):
    exercise_name = models.CharField(max_length=100, unique=True)
    calorie_burn_per_min = models.FloatField(default=.0)

    def __str__(self):
        return f'Id: {self.id}'


class FoodEaten(models.Model):
    date = models.DateField(auto_now_add=True, )
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodBook, on_delete=models.CASCADE)

    def __str__(self):
        return f'Id: {self.id}'


class ExerciseTaken(models.Model):
    date = models.DateField(auto_now_add=True, )
    duration = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(ExerciseBook, on_delete=models.CASCADE)

    def __str__(self):
        return f'Id: {self.id}'


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, )
    content = models.CharField(max_length=5000)
    title = models.CharField(max_length=100)
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)

    def __str__(self):
        return f'Id: {self.id}'


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, )
    content = models.CharField(max_length=1000)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_comment = models.ForeignKey("self", on_delete=models.CASCADE)

    def __str__(self):
        return f'Id: {self.id}'


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f'Id: {self.id}, Article id: {self.article}, \
                User id: {self.user}, comment id: {self.comment}'
