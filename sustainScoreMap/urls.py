# sustainScoreMap/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sustainscoremap'),  # Default route for your app
]