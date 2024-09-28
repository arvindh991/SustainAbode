# Create your views here.

# compareSuburbsMap/views.py

from django.http import HttpResponse
from django.shortcuts import render

# Landing page view
def landing_page(request):
    return render(request, 'landing_page.html')

def index(request):
    return render(request, 'compareSuburbsMap/compare.html')
