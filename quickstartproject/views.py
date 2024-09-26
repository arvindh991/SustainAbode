# sustainabode/views.py
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html')

    def index(request):
    return render(request, 'compareSuburbsMap/compare.html')
