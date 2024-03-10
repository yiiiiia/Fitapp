from django.urls import path

from .views import (AddFoodEatenView, FoodListView, UserRelatedDataView,
                    dashboard, food_daily, food_page, food_records,
                    metabolism_7days, metabolism_view)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('add_food_eaten', AddFoodEatenView.as_view(), name='add_food_eaten'),
    path('user-data/', UserRelatedDataView.as_view(), name='user-data'),
    path('foods/', FoodListView.as_view(), name='food-list'),
    path('food_page/', food_page, name='food_page'),
    path('metabolism/', metabolism_view, name='metabolism'),
    path('metabolism_7days/', metabolism_7days, name='metabolism_7days'),
    path('food_daily/', food_daily, name='food_daily'),
    path('food_records/', food_records, name='food_records'),
]
