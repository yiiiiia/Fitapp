import logging

from django.shortcuts import redirect, render

from UserProfile.views import login_required

from .forms import ExerciseBookForm


@login_required
def dashboard(request):
    # return render(request, 'graph.html', {'username': 'Felicity'})
    return render(request, 'dashboard.html', {'username': 'Felicity'})


@login_required
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


@login_required
def food_page(request):
    return render(request, 'food_page.html')
