from django.urls import path
from . import views

app_name = 'content_interaction'

urlpatterns = [
    path('article/add/', views.add_article, name='add_article'),
]
