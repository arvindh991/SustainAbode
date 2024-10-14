from django.contrib import admin
from django.urls import include, path
from . import views  # Import the views from the project folder

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Load the landing page from project views
    path('sustainscoremap/', include('sustainScoreMap.urls')),  # Link the app's URLs
    path('comparesuburbsmap/', include('compareSuburbsMap.urls')),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('housingdata_report/', views.housingdata_report, name='housingdata_report'),
    path('carbon_emission_report/', views.carbon_emission_report, name='carbon_emission_report'),
    path('transport_report/', views.transport_report, name='transport_report'),
    path('crime_report/',views.crime_report, name='crime_report')
]
