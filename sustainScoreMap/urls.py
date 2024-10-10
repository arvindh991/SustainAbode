# sustainScoreMap/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sustainscoremap'),  # Default route for sustainScoreMap
    path('compare/', views.compare_redirect, name='compare_redirect'),  # re-directed route to compare.html
]