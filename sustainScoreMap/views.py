# Create your views here.

# sustainScoreMap/views.py

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'sustainScoreMap/sustainscore.html')