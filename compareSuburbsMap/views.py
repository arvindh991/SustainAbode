# Create your views here.

# compareSuburbsMap/views.py

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'compareSuburbsMap/compare.html')
