from django.urls import path
from . import views

urlpatterns = [
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    # 添加更多 URL 模式
]
