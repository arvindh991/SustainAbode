"""sustainabode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views  # Import the views from the project folder

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Load the landing page from project views
    path('about/', views.about_page, name='about_page'),  # Load the about page from project views
    path('sustainscoremap/', include('sustainScoreMap.urls')),  # Link the app's URLs
    path('comparesuburbsmap/', include('compareSuburbsMap.urls')),
    path('admin/', admin.site.urls),
]
