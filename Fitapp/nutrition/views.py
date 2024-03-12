import random
import string
from datetime import datetime, timedelta

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DailyMetabolism, FoodBook, FoodEaten


class FoodEatenSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodEaten
        fields = ['id', 'user', 'food', 'amount', 'date']


class DailyMetabolismSerializer(serializers.ModelSerializer):
    bmr = serializers.SerializerMethodField()
    intake = serializers.SerializerMethodField()
    exercise_metabolism = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = DailyMetabolism
        fields = [
            'id', 'user', 'date', 'bmr', 'intake', 'exercise_metabolism',
            'total'
        ]

    def get_bmr(self, obj):
        return round(obj.bmr, 1)

    def get_intake(self, obj):
        return round(obj.intake, 1)

    def get_exercise_metabolism(self, obj):
        return round(obj.exercise_metabolism, 1)

    def get_total(self, obj):
        return round(obj.total, 1)


class FoodBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodBook
        fields = [
            'id', 'food_type', 'food_name', 'image', 'calories_per_gram',
            'protein_per_gram', 'fat_per_gram', 'carbohydrate_per_gram',
            'other_per_gram'
        ]


class FoodListView(APIView):
    """
    API view to list all foods or filter them based on a search query.
    """

    def get(self, request):
        search_query = request.query_params.get('search', None)
        if search_query:
            foods = FoodBook.objects.filter(
                Q(food_name__icontains=search_query)
                | Q(food_type__icontains=search_query))
        else:
            foods = FoodBook.objects.all()
        serializer = FoodBookSerializer(foods,
                                        many=True,
                                        context={'request': request})
        return Response(serializer.data)


class AddFoodEatenView(APIView):
    """
    API view for adding a food item to the user's eaten food list.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        food_id = request.data.get('food')
        amount = request.data.get('amount')
        date = request.data.get('date') or timezone.now().date()

        food = FoodBook.objects.get(id=food_id)
        FoodEaten.objects.create(user=user,
                                 food=food,
                                 amount=amount,
                                 date=date)

        food_calories = round(food.calories_per_gram * amount, 1)
        return JsonResponse({'message': 'Food added successfully', "calories": food_calories})


class UserRelatedDataView(APIView):
    """
    API view to retrieve food eaten by the user and their daily metabolism data.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        foods_eaten = FoodEaten.objects.filter(user=request.user)
        daily_metabolism = DailyMetabolism.objects.filter(user=request.user)

        foods_eaten_serializer = FoodEatenSerializer(foods_eaten, many=True)
        daily_metabolism_serializer = DailyMetabolismSerializer(
            daily_metabolism, many=True)

        return Response({
            'foods_eaten': foods_eaten_serializer.data,
            'daily_metabolism': daily_metabolism_serializer.data
        })


class FoodPageView(APIView):
    """
    API view to render the food exercise page for authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        letters = string.digits
        q = ''.join(random.choice(letters) for i in range(10))

        return render(
            request, 'food_exercise.html', {
                'page_type': 'food',
                'username': user.get_username(),
                'q': q,
            })


class MetabolismView(APIView):
    """
    API view to retrieve the user's metabolism data for the current day.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        metabolisms = DailyMetabolism.objects.filter(user=request.user,
                                                     date=today)
        return Response(
            metabolisms.values('id', 'bmr', 'intake', 'exercise_metabolism',
                               'total'))


class Metabolism7DaysView(APIView):
    """
    API view to retrieve the user's metabolism data for the last 7 days.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        metabolisms = DailyMetabolism.objects.filter(
            user=request.user, date__range=[week_ago, today])

        serializer = DailyMetabolismSerializer(metabolisms, many=True)
        return Response(serializer.data)


class FoodDailyView(APIView):
    """
    API view to calculate and retrieve the nutrient percentages of the foods eaten by the user for the current day.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.now().date()
        foods_eaten_today = FoodEaten.objects.filter(user=request.user,
                                                     date=today)

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
            total_nutrients[
                'carbohydrate'] += food.carbohydrate_per_gram * amount_grams
            total_nutrients['protein'] += food.protein_per_gram * amount_grams
            total_nutrients['other'] += food.other_per_gram * amount_grams

        total = sum(total_nutrients.values())
        if total > 0:
            percentages = {
                key: round((value / total * 100), 1)
                for key, value in total_nutrients.items()
            }
        else:
            percentages = {key: 0 for key in total_nutrients}

        return Response(percentages)


def food_records(request):
    """
    Django view to retrieve food records for an authenticated user.
    """
    if request.user.is_authenticated:
        food_eaten_records = FoodEaten.objects.filter(
            user=request.user).select_related('food').order_by('-date')
        serializer = FoodEatenSerializer(food_eaten_records, many=True)
        return JsonResponse({'food_eaten_records': serializer.data},
                            safe=False)
    else:
        return JsonResponse({'food_eaten_records': []})
