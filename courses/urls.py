from django.urls import path
from .views import CourseRecommendationView

urlpatterns = [
    path("recommendations/", CourseRecommendationView.as_view(), name="course-recommendations"),
]
