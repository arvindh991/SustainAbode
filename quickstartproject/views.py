# sustainabode/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def landing_page(request):
    return render(request, 'landing_page.html')