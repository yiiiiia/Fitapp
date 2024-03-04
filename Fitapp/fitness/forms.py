from django import forms
from .models import ExerciseBook

class ExerciseBookForm(forms.ModelForm):
    class Meta:
        model = ExerciseBook
        fields = ['exercise_name', 'calories_burned_per_min']
