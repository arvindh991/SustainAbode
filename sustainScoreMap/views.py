# Create your views here.

# sustainScoreMap/views.py

from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserInputForm
from .ml_model import score_model
from django.conf import settings 

def index(request):
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
            }

            print(user_input)

            # Call the ML model and get the GeoJSON file
            geojson_url = score_model(user_input)

            print("I have recieved an output from the ML_model")

            print(f"Here is where my file is stored {geojson_url}")

            # Pass the form and GeoJSON path back to the template
            return render(request, 'sustainScoreMap/sustainscore.html', {
                'form': form,
                'geojson_url': geojson_url,
                'mapbox_api_key': settings.MAPBOX_API_KEY
            })

    else:
        form = UserInputForm()

    return render(request, 'sustainScoreMap/sustainscore.html', {'form': form})