# forms.py
from django import forms

class UserInputForm(forms.Form):
    HOUSE_TYPE_CHOICES = [('h', 'House'), ('u', 'Unit')]
    
    # Set a default value for house_type as 'House'
    house_type = forms.ChoiceField(choices=HOUSE_TYPE_CHOICES, label='House Type', initial='h')

    # Set a default value for rooms (e.g., 3)
    rooms = forms.IntegerField(min_value=1, max_value=10, label='Number of Rooms', initial=3)

    # Set a default value for distance (e.g., 10 km)
    distance = forms.IntegerField(min_value=5, max_value=50, label='Preferred Distance (km)', initial=10)

    # Set the default to False for the BooleanField affordable (no need to specify explicitly since `False` is default)
    affordable = forms.BooleanField(required=False, label='Affordable Housing', initial=False)

    # Set the default to False for prefer_parks
    prefer_parks = forms.BooleanField(required=False, label='Prefer Parks', initial=False)

    # Add new fields for user preferences for bus and carpark
    prefer_bus = forms.BooleanField(required=False, label='Prefer Bus Service', initial=False)
    prefer_carpark = forms.BooleanField(required=False, label='Prefer Train Carpark Availability', initial=False)

    # Add new fields for user preferences for air quality and co2 emissions
    prefer_good_air_quality_low_co2_emission = forms.BooleanField(required=False, label='Prefer Low CO2', initial=False)
    prefer_less_crime = forms.BooleanField(required=False, label='Prefer Less Crime', initial=False)