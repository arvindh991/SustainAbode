from django import forms

class UserInputForm(forms.Form):
    HOUSE_TYPE_CHOICES = [('h', 'House'), ('u', 'Unit')]

    # Set a default value for house_type as 'House' and add a tooltip
    house_type = forms.ChoiceField(
        choices=HOUSE_TYPE_CHOICES,
        label='House Type',
        initial='h',
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'title': 'Choose whether you want a house or a unit.'  # Tooltip
        })
    )

    # Set a default value for rooms (e.g., 3) and add a tooltip
    rooms = forms.IntegerField(
        min_value=1,
        max_value=10,
        label='Number of Rooms',
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'title': 'Select the number of rooms you need.'  # Tooltip
        })
    )

    # Set a default value for distance (e.g., 10 km) and add a tooltip
    distance = forms.IntegerField(
        min_value=5,
        max_value=50,
        label='Suburb distance from CBD (KM)',
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'title': 'Most of the further suburbs from the CBD are greener. Please try to input how far you want to live from the CBD.'  # Tooltip
        })
    )

    # Set the default to False for affordable housing and add a tooltip
    affordable = forms.BooleanField(
        required=False,
        label='Prioritise suburbs with affordable house prices',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'This filter helps you identify suburbs with affordable housing closer to the median price.'  # Tooltip
        })
    )

    # Set the default to False for prefer_parks and add a tooltip
    prefer_parks = forms.BooleanField(
        required=False,
        label='I prefer to go for walks in Parks',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Average green park area size is 3344 sqm. Selecting this filter will show suburbs with larger park areas than average.'  # Tooltip
        })
    )

    # Add new fields for user preferences for bus service and add a tooltip
    prefer_bus = forms.BooleanField(
        required=False,
        label='Prioritise suburbs with frequent bus services',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Melbourne suburbs have 43 stations on average. Selecting this filter will prioritise suburbs with more stations.'  # Tooltip
        })
    )

    # Add new fields for user preferences for car parking and add a tooltip
    prefer_carpark = forms.BooleanField(
        required=False,
        label='I prefer to park my car near train stations',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Suburbs in Melbourne have 677 general parking spaces near train stations. Select this filter to prioritise suburbs with more parking spaces.'  # Tooltip
        })
    )

    # Add new fields for user preferences for air quality and add a tooltip
    prefer_good_air_quality_low_co2_emission = forms.BooleanField(
        required=False,
        label='Prioritise suburbs with low carbon dioxide emission',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Selecting this filter will bring the suburbs with the best air quality.'  # Tooltip
        })
    )

    # Add new fields for user preferences for crime rates and add a tooltip
    prefer_less_crime = forms.BooleanField(
        required=False,
        label='I want to live in suburbs where frequency of crimes are lower',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Average crime incidents a year in Melbourne suburbs is 2676. Select this filter to prioritise suburbs with lower crime rates.'  # Tooltip
        })
    )
