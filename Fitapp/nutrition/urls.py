from django.urls import path
from .views import UserRelatedDataView, AddFoodEatenView, FoodListView, show_add_food_eaten_page
from . import views

urlpatterns = [
    path('add_food/', views.add_food, name='add_food'),
    path('add-food-eaten', show_add_food_eaten_page, name='add-food-eaten'),
    path('add_food_eaten', AddFoodEatenView.as_view(), name='add_food_eaten'),
    path('user-data/', UserRelatedDataView.as_view(), name='user-data'),
    path('foods/', FoodListView.as_view(), name='food-list'),
    path('foodlist/', views.foodlist, name='foodlist'),
    path('metabolism/', views.metabolism_view, name='metabolism'),
    path('metabolism_7days/', views.metabolism_7days, name='metabolism_7days'),
]
