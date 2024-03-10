import random
import string
from datetime import timedelta

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from UserProfile.views import login_required

from .models import DailyMetabolism, FoodBook, FoodEaten


class FoodListView(APIView):
    def get(self, request):
        foods = FoodBook.objects.all()
        data = [{"id": food.id, "name": food.food_name} for food in foods]
        return Response(data)


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


@login_required
def dashboard(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    letters = string.digits
    # TODO get metabolism related data
    q = ''.join(random.choice(letters) for i in range(10))
    ctx = {
        'username': user.get_username(),
        'exercise_metabolism': 400,
        'bmr': 150,
        'intake': 200,
        'total': 200 - 400 - 150,
        'q': q
    }
    return render(request, 'dashboard.html', ctx)


@login_required
def food_page(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    letters = string.digits
    q = ''.join(random.choice(letters) for i in range(10))
    return render(request, 'food_exercise.html', {'food_page': True, 'page_type': 'food', 'q': q, 'username': user.get_username()})


def metabolism_view(request):
    today = timezone.now().date()
    metabolisms = DailyMetabolism.objects.filter(user=request.user, date=today).values(
        'id', 'bmr', 'intake', 'exercise_metabolism', 'total')  # 获取所有记录的特定字段
    metabolisms_list = list(metabolisms)  # 将QuerySet转换为列表
    return JsonResponse(metabolisms_list, safe=False)


def metabolism_7days(request):
    # 7天柱状图
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    metabolisms = DailyMetabolism.objects.filter(user=request.user, date__range=[
                                                 week_ago, today]).values('date', 'bmr', 'intake', 'exercise_metabolism', 'total')
    metabolisms_7dayslist = list(metabolisms)
    return JsonResponse(metabolisms_7dayslist, safe=False)


def food_daily(request):
    # 饼图的
    if request.user.is_authenticated:
        food_eaten = FoodEaten.objects.filter(user=request.user).values('food', 'amount',
                                                                        'date')  # 假设FoodBook模型有一个'name'字段
        return JsonResponse(list(food_eaten), safe=False)
    return JsonResponse([], safe=False)


def food_records(request):
    if request.user.is_authenticated:
        food_eaten_records = list(FoodEaten.objects.filter(user=request.user).select_related('food').order_by('-date').values('food__food_name', 'amount',
                                  'date', 'food__calories_per_gram', 'food__protein_per_gram', 'food__fat_per_gram', 'food__carbohydrate_per_gram', 'food__other_per_gram'))
        return JsonResponse({'food_eaten_records': food_eaten_records}, safe=False)
    else:
        return JsonResponse({'food_eaten_records': []})
