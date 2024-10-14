# sustainabode/views.py

from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html')

def about(request):
    return render(request, 'about.html')

def housingdata_report(request):
    return render(request, 'housingdata_report.html')

def crime_report(request):
    return render(request, 'crime_report.html')

def transport_report(request):
    return render(request, 'transport_report.html')

def carbon_emission_report(request):
    return render(request, 'carbon_emission_report.html')