# sustainabode/views.py
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html')

def about_page(request):
    return render(request, 'about_page.html')