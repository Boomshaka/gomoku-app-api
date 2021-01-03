from django.urls import path

from .views import (
    GameAPIView,
    GameDetails
)


urlpatterns = [
    path('game/', GameAPIView.as_view()),
    path('game/<uuid:pk>/', GameDetails.as_view())
]
