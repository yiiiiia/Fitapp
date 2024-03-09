import random
import string

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from UserProfile.views import login_required

from .forms import DailyMetabolismForm, FoodBookForm, FoodEatenForm
from .models import DailyMetabolism, FoodBook, FoodEaten


class FoodListView(APIView):
    def get(self, request):
        foods = FoodBook.objects.all()
        data = [{"id": food.id, "name": food.food_name} for food in foods]
        return Response(data)


def show_add_food_eaten_page(request):
    return render(request, 'add_food_eaten.html')


class AddFoodEatenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        food_id = request.data.get('food')
        amount = request.data.get('amount')
        date = request.data.get('date') or timezone.now().date()

        food = FoodBook.objects.get(id=food_id)
        FoodEaten.objects.create(user=user, food=food,
                                 amount=amount, date=date)

        return JsonResponse({'message': 'Food added successfully'})


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


@login_required
def food_page(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    letters = string.digits
    q = ''.join(random.choice(letters) for i in range(10))
    return render(request, 'food_exercise.html', {'food_page': True, 'page_type': 'food', 'q': q, 'username': user.get_username()})
