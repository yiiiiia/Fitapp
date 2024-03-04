from django import forms
from .models import FoodEaten, DailyMetabolism

class FoodEatenForm(forms.ModelForm):
    class Meta:
        model = FoodEaten
        fields = ['food', 'amount', 'date']

class DailyMetabolismForm(forms.ModelForm):
    class Meta:
        model = DailyMetabolism
        fields = ['date', 'bmr', 'intake', 'exercise_metabolism', 'total']
