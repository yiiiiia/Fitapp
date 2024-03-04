from django.urls import path
from .views import UserRelatedDataView
from . import views

urlpatterns = [
    path('add_food_eaten/', views.add_food_eaten, name='add_food_eaten'),
    path('user-data/', UserRelatedDataView.as_view(), name='user-data'),
]
