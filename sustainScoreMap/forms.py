from django import forms

class UserInputForm(forms.Form):
    HOUSE_TYPE_CHOICES = [('h', 'House'), ('u', 'Unit')]

    # House Type field
    house_type = forms.ChoiceField(
        choices=HOUSE_TYPE_CHOICES,
        label='House Type',
        initial='h',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': 'Choose whether you want a house or a unit.'
        })
    )

    # Number of Rooms field
    rooms = forms.IntegerField(
        min_value=1,
        max_value=10,
        label='Number of Rooms',
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'title': 'Select the number of rooms you need.'
        })
    )

    # Suburb Distance field
    distance = forms.IntegerField(
        min_value=5,
        max_value=50,
        label='Suburb distance from CBD (KM)',
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'title': 'Most of the further suburbs from the CBD are greener. Please try to input how further you want to live from the CBD.'
        })
    )

    # Affordable Housing field
    affordable = forms.BooleanField(
        required=False,
        label='Prioritise suburbs with affordable house prices',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'This filter highlights suburbs with affordable houses compared to the Melbourne median prices. Median prices for Melbourne are:\nHouses: AUD 1,107,110\nUnit: AUD 915,876\nTown House: AUD 636,904'
        })
    )

    # Prefer Parks field
    prefer_parks = forms.BooleanField(
        required=False,
        label='I prefer to go for walks in Parks',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Average green park area size is 3344 square meters. Selecting this filter will show suburbs which have more park areas than average.'
        })
    )

    # Prefer Bus Service field
    prefer_bus = forms.BooleanField(
        required=False,
        label='Prioritise suburbs with frequent bus services',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Melbourne Suburbs has 43 stops on average. Selecting this filter will prioritise suburbs with more number of bus stops on average.'
        })
    )

    # Prefer Train Carpark Availability field
    prefer_carpark = forms.BooleanField(
        required=False,
        label='I prefer to park my car near train stations',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Suburbs in Melbourne have 677 general parking spaces near train stations. Select this filter to prioritise suburbs with more parking spaces than average.'
        })
    )

    # Prefer Good Air Quality field
    prefer_good_air_quality_low_co2_emission = forms.BooleanField(
        required=False,
        label='Prioritise suburbs with low carbon dioxide emission',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Select this filter to highlight suburbs with the best air quality and lower carbon dioxide emissions, offering a healthier living environment.'
        })
    )

    # Prefer Less Crime field
    prefer_less_crime = forms.BooleanField(
        required=False,
        label='I want to live in suburbs where frequency of criminal incidents are lower',
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'title': 'Average crime incidents a year in Melbourne Suburbs is 2676. Select this filter to bring up suburbs which have lower crime rates than average.\nThis filter highlights suburbs with fewer incidents of serious crimes like burglary, criminal damage, and offences against persons, compared to the Melbourne average. Use this to prioritise safer neighbourhoods with lower crime rates.'
        })
    )
