# sustainScoreMap/views.py

from django.shortcuts import render, redirect
from .forms import UserInputForm
from .ml_model import score_model
from django.conf import settings

# sustainScoreMap/views.py

from django.shortcuts import render, redirect
from .forms import UserInputForm
from .ml_model import score_model
from django.conf import settings

def index(request):
    mapbox_api_key = settings.MAPBOX_API_KEY
    geojson_url = None
    suburbs = []

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

            # Save the form data in the session to prepopulate later
            request.session['user_input'] = user_input

            # Call the ML model to get the GeoJSON and top suburbs
            geojson_url, suburbs = score_model(user_input)

            # Store the suburbs and geojson_url in session for later use
            request.session['suburb_list'] = suburbs
            request.session['geojson_url'] = geojson_url

            print("#################### SESSION DATA STORED ####################")

    else:
        form = UserInputForm()

    return render(request, 'sustainScoreMap/sustainscore.html', {
        'form': form,
        'geojson_url': geojson_url,
        'mapbox_api_key': mapbox_api_key,
        'suburbs': suburbs
    })


# separate view to handle the "Compare Now" redirection logic without regenerating the geoJSON
def compare_redirect(request):
    # Ensure that the session data is still available
    if 'suburb_list' in request.session and 'geojson_url' in request.session:
        request.session['from_sustainscore'] = True  # Set flag
        print("#################### SESSION Flag set to TRUE ####################")
        return redirect('comparesuburbsmap')  # Redirect to the compare page
    else:
        print("#################### No session data :( ####################")
        return redirect('index')  # If session data is missing, redirect to sustainScore page
