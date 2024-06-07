# api/urls.py
from django.urls import path
from .views import SerialValidationView, SessionValidationView

urlpatterns = [
    path('validate-serial/', SerialValidationView.as_view(), name='validate-serial'),
    path('validate-session/', SessionValidationView.as_view(), name='validate-session'),
]