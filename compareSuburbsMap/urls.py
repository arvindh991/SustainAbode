# compareSuburbsMap/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.compare_view, name='comparesuburbsmap'),  # Default route for your app
]