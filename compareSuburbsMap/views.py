# compareSuburbsMap/views.py

from django.shortcuts import render
from sustainScoreMap.forms import UserInputForm
from sustainScoreMap.ml_model import score_model
from django.conf import settings

def compare_view(request):
    # Default settings
    geojson_url = None
    suburb_list = []
    mapbox_api_key = settings.MAPBOX_API_KEY

    # Prepopulate form if user comes from sustainscore
    if request.session.get('from_sustainscore', False):
        # Retrieve the saved data from the session (set in sustainscore view)
        suburb_list = request.session.get('suburb_list', [])
        geojson_url = request.session.get('geojson_url', None)
        user_input = request.session.get('user_input', {})

        # Pre-populate the form with saved user_input data
        form = UserInputForm(initial=user_input)
        print(user_input)
        print("#################### SESSION DATA RETRIEVED ####################")

        # Reset the flag to indicate the user has moved away from sustainscore page
        request.session['from_sustainscore'] = False

    else:
        # When visiting the page for the first time directly (not from sustainscore), render an empty form
        form = UserInputForm()

    # Handle form resubmission on the compare page
    if request.method == 'POST':
        print("#################### FORM RESUBMITTED ON COMPARE PAGE ####################")

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


            # Call the ML model to get new GeoJSON and suburb list
            geojson_url, suburb_list = score_model(user_input)

    return render(request, 'compareSuburbsMap/compare.html', {
        'form': form,
        'geojson_url': geojson_url,
        'mapbox_api_key': mapbox_api_key,
        'suburb_list': suburb_list
    })
