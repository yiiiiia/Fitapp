from django.urls import path

from . import views
from .views import (AddFoodEatenView, FoodListView, UserRelatedDataView,
                    show_add_food_eaten_page)

urlpatterns = [
    path('add_food/', views.add_food, name='add_food'),
    path('add-food-eaten', show_add_food_eaten_page, name='add-food-eaten'),
    path('add_food_eaten', AddFoodEatenView.as_view(), name='add_food_eaten'),
    path('user-data/', UserRelatedDataView.as_view(), name='user-data'),
    path('foods/', FoodListView.as_view(), name='food-list'),
    path('food_page/', views.food_page, name='food_page'),
]
