# compareSuburbsMap/views.py

from django.http import HttpResponse
from django.shortcuts import render
from sustainScoreMap.forms import UserInputForm
from sustainScoreMap.ml_model import score_model
from django.conf import settings
import pandas as pd

import logging
logger = logging.getLogger(__name__)

def index(request):

    mapbox_api_key = settings.MAPBOX_API_KEY
    geojson_url = None
    top_suburbs = []
    suburb_reports = {}
    suburb_list = ""
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            user_input = {
                'type': form.cleaned_data['house_type'],
                'rooms': form.cleaned_data['rooms'],
                'distance': form.cleaned_data['distance'],
                'affordable': form.cleaned_data['affordable'],
                'prefer_parks': form.cleaned_data['prefer_parks'],
                'prefer_bus': form.cleaned_data['prefer_bus'],
                'prefer_carpark': form.cleaned_data['prefer_carpark'],
                'prefer_good_air_quality_low_co2_emission': form.cleaned_data['prefer_good_air_quality_low_co2_emission'],
                'prefer_less_crime': form.cleaned_data['prefer_less_crime'],
            }

        # Call the ML model to get the GeoJSON and top suburbs
        geojson_url, top_suburbs = score_model(user_input)
    
        # For each suburb, generate the URLs for the reports (piechart, price_distribution, etc.)
        for suburb in top_suburbs:
            # Replace whitespace with underscores in the suburb name
            suburb_with_underscore = suburb.title().replace(' ', '_')

            suburb_report_urls = {
                'piechart': f"{settings.AZURE_CONTAINER_URL}/piechart_{suburb_with_underscore}.png",
                'price_distribution': f"{settings.AZURE_CONTAINER_URL}/price_distribution_{suburb_with_underscore}.png"
            }

            # Add the URLs to the main report_urls dictionary with suburb as the key
            suburb_reports[suburb_with_underscore] = suburb_report_urls
    
        logger.info(f"Top suburbs: {top_suburbs}")
        logger.info(f"Suburb reports: {suburb_reports}")
        logger.info(f"GeoJSON URL: {geojson_url}")
        logger.info(f"mapbox_api_key: {mapbox_api_key}")
        suburb_list = ", ".join(f"'{x}'" for x in top_suburbs)

    else:
        form = UserInputForm()

    return render(request, 'compareSuburbsMap/compare.html', {
        'form': form,
        'geojson_url': geojson_url,
        'mapbox_api_key': mapbox_api_key,
        'suburb_reports': suburb_reports,
        'suburb_list': suburb_list,
    })
