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


from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from datetime import datetime

class FoodEatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodEaten
        fields = ['id', 'user', 'food', 'amount', 'date']

class DailyMetabolismSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMetabolism
        fields = ['id', 'user', 'date', 'bmr', 'intake', 'exercise_metabolism', 'total']

class FoodBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodBook
        fields = ['id', 'food_type', 'food_name', 'calories_per_gram', 'protein_per_gram', 'fat_per_gram', 'carbohydrate_per_gram', 'other_per_gram']

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
        foods_eaten = FoodEaten.objects.filter(user=request.user)
        daily_metabolism = DailyMetabolism.objects.filter(user=request.user)

        foods_eaten_serializer = FoodEatenSerializer(foods_eaten, many=True)
        daily_metabolism_serializer = DailyMetabolismSerializer(daily_metabolism, many=True)

        return Response({
            'foods_eaten': foods_eaten_serializer.data,
            'daily_metabolism': daily_metabolism_serializer.data
        })


@login_required
def food_page(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    letters = string.digits
    q = ''.join(random.choice(letters) for i in range(10))
    return render(request, 'food_exercise.html', {'food_page': True, 'page_type': 'food', 'q': q, 'username': user.get_username()})



class MetabolismView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        metabolisms = DailyMetabolism.objects.filter(user=request.user, date=today)
        return Response(metabolisms.values('id', 'bmr', 'intake', 'exercise_metabolism', 'total'))


class Metabolism7DaysView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        metabolisms = DailyMetabolism.objects.filter(user=request.user, date__range=[week_ago, today])
        
        serializer = DailyMetabolismSerializer(metabolisms, many=True)
        return Response(serializer.data)

class FoodDailyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.now().date()
        foods_eaten_today = FoodEaten.objects.filter(user=request.user, date=today)

        total_nutrients = {
            'fat': 0,
            'carbohydrate': 0,
            'protein': 0,
            'other': 0
        }

        for food_eaten in foods_eaten_today:
            food = food_eaten.food
            amount_grams = food_eaten.amount
            total_nutrients['fat'] += food.fat_per_gram * amount_grams
            total_nutrients['carbohydrate'] += food.carbohydrate_per_gram * amount_grams
            total_nutrients['protein'] += food.protein_per_gram * amount_grams
            total_nutrients['other'] += food.other_per_gram * amount_grams

        total = sum(total_nutrients.values())
        if total > 0:
            percentages = {key: round((value / total * 100), 1) for key, value in total_nutrients.items()}
        else:
            percentages = {key: 0 for key in total_nutrients}

        return Response(percentages)

def food_records(request):
    if request.user.is_authenticated:
        food_eaten_records = list(FoodEaten.objects.filter(user=request.user).select_related('food').order_by('-date').values('food__food_name', 'amount',
                                  'date', 'food__calories_per_gram', 'food__protein_per_gram', 'food__fat_per_gram', 'food__carbohydrate_per_gram', 'food__other_per_gram'))
        return JsonResponse({'food_eaten_records': food_eaten_records}, safe=False)
    else:
        return JsonResponse({'food_eaten_records': []})
