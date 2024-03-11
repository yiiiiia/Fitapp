from django.urls import path

from .views import (AddFoodEatenView, FoodListView, UserRelatedDataView,
                    show_add_food_eaten_page, MetabolismView, Metabolism7DaysView, FoodDailyView)

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('add_food/', views.add_food, name='add_food'),
    path('add-food-eaten', show_add_food_eaten_page, name='add-food-eaten'),
    path('add_food_eaten', AddFoodEatenView.as_view(), name='add_food_eaten'),
    path('user-data/', UserRelatedDataView.as_view(), name='user-data'),
    path('foods/', FoodListView.as_view(), name='food-list'),
    path('food_page/', views.food_page, name='food_page'),
    path('metabolism/', MetabolismView.as_view(), name='metabolism'),
    path('metabolism_7days/', Metabolism7DaysView.as_view(), name='metabolism_7days'),
    path('food_daily/', FoodDailyView.as_view(), name='food_daily'),
    path('food_records/', views.food_records, name='food_records'),
]
