from django.contrib import admin
from .models import FoodEaten, DailyMetabolism, FoodBook

admin.site.register(FoodEaten)
admin.site.register(DailyMetabolism)
admin.site.register(FoodBook)
