# sustainScoreMap/views.py

from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserInputForm
from .ml_model import score_model
from django.conf import settings
from .reports import generate_and_save_reports_for_suburb
import os
import pandas as pd

def index(request):

    mapbox_api_key = settings.MAPBOX_API_KEY
    geojson_url = None
    suburb_reports = {}
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
            }

        # Call the ML model to get the GeoJSON and top suburbs
        geojson_url, top_suburbs, geo_df = score_model(user_input)

        # Define the base data directory
        data_dir = os.path.join(settings.BASE_DIR, 'data')

        # Loading the house price dataset from the data folder
        melbourne_data = pd.read_csv(os.path.join(data_dir, 'MELBOURNE_HOUSE_PRICES_LESS_CLEAN.csv'))

        for suburb in top_suburbs:
            suburb_reports[suburb] = generate_and_save_reports_for_suburb(suburb, geo_df, melbourne_data)

    else:
        form = UserInputForm()

    return render(request, 'sustainScoreMap/sustainscore.html', {
        'form': form,
        'geojson_url': geojson_url,
        'mapbox_api_key': mapbox_api_key,
        'suburb_reports': suburb_reports
    })
