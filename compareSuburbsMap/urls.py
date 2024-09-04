# compareSuburbsMap/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='comparesuburbsmap'),  # Default route for your app
]