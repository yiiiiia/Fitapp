from django.shortcuts import render, redirect
from .models import FoodEaten, DailyMetabolism, FoodBook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import FoodEatenForm, DailyMetabolismForm, FoodBookForm

def add_food_eaten(request):
    if request.method == 'POST':
        form = FoodEatenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_view')
    else:
        form = FoodEatenForm()
    
    return render(request, 'add_food_eaten.html', {'form': form})

class UserRelatedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取当前登录的用户
        user = request.user

        # 获取与该用户相关的 FoodEaten 和 DailyMetabolism 数据
        foods_eaten = FoodEaten.objects.filter(user=user)
        daily_metabolism = DailyMetabolism.objects.filter(user=user)

        # 返回响应
        return Response({
            'foods_eaten': foods_eaten,
            'daily_metabolism': daily_metabolism
        })
    
def add_food(request):
    print("进入了 add_food 视图")
    if request.method == 'POST':
        form = FoodBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_view_name')
    else:
        form = FoodBookForm()
    return render(request, 'add_food.html', {'form': form})