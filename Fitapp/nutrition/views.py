from django.shortcuts import render, redirect
from .models import FoodEaten, DailyMetabolism, FoodBook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.http import JsonResponse
from .forms import FoodEatenForm, DailyMetabolismForm, FoodBookForm

from datetime import timedelta
from django.utils import timezone


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
        FoodEaten.objects.create(user=user, food=food, amount=amount, date=date)

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


def foodlist(request):
    if request.method == "GET":
        return render(request,"food_list.html")



def metabolism_view(request):
    today = timezone.now().date()
    metabolisms = DailyMetabolism.objects.filter(user=request.user, date=today).values('id', 'bmr', 'intake', 'exercise_metabolism', 'total')  # 获取所有记录的特定字段
    metabolisms_list = list(metabolisms)  # 将QuerySet转换为列表
    return JsonResponse(metabolisms_list, safe=False)

def metabolism_7days(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    metabolisms = DailyMetabolism.objects.filter(user=request.user, date__range=[week_ago, today]).values('date', 'bmr', 'intake', 'exercise_metabolism', 'total')
    metabolisms_7dayslist = list(metabolisms)
    return JsonResponse(metabolisms_7dayslist, safe=False)