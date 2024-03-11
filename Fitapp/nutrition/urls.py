from django.urls import path

from .views import (AddFoodEatenView, FoodListView, FoodPageView, UserRelatedDataView,
                    MetabolismView, Metabolism7DaysView, FoodDailyView)

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('add_food_eaten/', AddFoodEatenView.as_view(), name='add_food_eaten'),
    path('user-data/', UserRelatedDataView.as_view(), name='user-data'),
    path('food_list/', FoodListView.as_view(), name='food_list'),
    path('food_page/', FoodPageView.as_view(), name='food_page'),
    path('metabolism/', MetabolismView.as_view(), name='metabolism'),
    path('metabolism_7days/', Metabolism7DaysView.as_view(), name='metabolism_7days'),
    path('food_daily/', FoodDailyView.as_view(), name='food_daily'),
    path('food_records/', views.food_records, name='food_records'),
]
