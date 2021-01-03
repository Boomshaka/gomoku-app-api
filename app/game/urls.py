from django.urls import path

from .views import (
    GameAPIView
)


urlpatterns = [
    path('game/', GameAPIView.as_view()),
]
