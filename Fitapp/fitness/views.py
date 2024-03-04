from django.shortcuts import render, redirect
from .forms import ExerciseBookForm
from .models import ExerciseBook

def add_exercise(request):
    print("进入了 add_exercise 视图")
    if request.method == 'POST':
        form = ExerciseBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_view_name')
    else:
        form = ExerciseBookForm()
    return render(request, 'add_exercise.html', {'form': form})

