from django.utils import timezone
from nutrition.models import DailyMetabolism
from .models import UserProfile

class DailyMetabolismMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.update_daily_metabolism(request.user)
        return response

    def update_daily_metabolism(self, user):
        if user.is_authenticated:
            today = timezone.now().date()
            profile, created = UserProfile.objects.get_or_create(user=user)
            bmr_formula = self.calculate_bmr(profile)
            print("bmr_formula:", bmr_formula)
            daily_metabolism, created = DailyMetabolism.objects.get_or_create(
                user=user, 
                date=today, 
                defaults={'bmr': bmr_formula, 'intake': 0, 'exercise_metabolism': 0, 'total': 0}
            )

            if not created:
                daily_metabolism.bmr = bmr_formula
                daily_metabolism.total = daily_metabolism.intake - bmr_formula - daily_metabolism.exercise_metabolism
                daily_metabolism.save()

    def calculate_bmr(self, profile):
        if not all([profile.age, profile.gender, profile.height, profile.weight]):
            return 0  # Return 0 if any profile detail is missing

        # BMR calculation logic remains unchanged
        bmr_formula = 88.362 + (13.397 * profile.weight) + (4.799 * profile.height) - (5.677 * profile.age) \
            if profile.gender == 'male' \
            else 447.593 + (9.247 * profile.weight) + (3.098 * profile.height) - (4.330 * profile.age)
        return bmr_formula
