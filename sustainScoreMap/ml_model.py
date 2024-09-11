import os
import pandas as pd
import geopandas as gpd
from django.conf import settings

# # Example of user inputs (these would be dynamic in a real application)
#     user_input = {
#         'type': 'h',  # house or unit
#         'rooms': 3,   # preferred number of rooms # make sure user does not input any number less than 3
#         'distance': 10,  # preferred distance # make sure user does not input any number less than 5
#         'affordable': True,  # if affordability should be maximized # preferred input: True/False
#         'prefer_parks': False  # if park preferences are included # preferred input: True/False
#     }

def score_model(user_input):
    # Define the base data directory
    data_dir = os.path.join(settings.BASE_DIR, 'data')

    media_dir = os.path.join(settings.BASE_DIR, 'media')

    geojson_dir = os.path.join(media_dir, 'geoJSON')

    # Loading the house price dataset from the data folder
    melbourne_data = pd.read_csv(os.path.join(data_dir, 'MELBOURNE_HOUSE_PRICES_LESS_CLEAN.csv'))

    # Filter data based on user inputs
    filtered_data = melbourne_data[
        (melbourne_data['Type'] == user_input['type']) &
        (melbourne_data['Rooms'].between(user_input['rooms'] - 2, user_input['rooms'] + 2)) &
        (melbourne_data['Distance'].between(user_input['distance'] - 5, user_input['distance'] + 5)) &
        (melbourne_data['Distance'] > 4)
    ]

    # If affordability is preferred, filter for prices below the median
    if user_input['affordable']:
        median_price = filtered_data['Price'].median()
        filtered_data = filtered_data[filtered_data['Price'] <= median_price]

    # Aggregate data by suburb
    suburb_rank = filtered_data.groupby('Suburb').agg(
        HouseCount=('Suburb', 'size'),  # Count of houses
        AveragePrice=('Price', 'mean'),  # Average house price
        AverageDistance=('Distance', 'mean')  # Average distance
    ).reset_index()

    # Rank the suburbs by house count, average price, and average distance
    suburb_rank['Rank_HouseCount'] = suburb_rank['HouseCount'].rank(ascending=False, method='min')  # More houses -> higher rank
    suburb_rank['Rank_AveragePrice'] = suburb_rank['AveragePrice'].rank(ascending=True, method='min')  # Lower price -> higher rank
    suburb_rank['Rank_AverageDistance'] = suburb_rank['AverageDistance'].rank(ascending=True, method='min')  # Closer distance -> higher rank

    # Total rank (sum of ranks across metrics)
    suburb_rank['TotalRank'] = suburb_rank['Rank_HouseCount'] + suburb_rank['Rank_AveragePrice'] + suburb_rank['Rank_AverageDistance']

    # Sort suburbs by their total rank
    suburb_rank = suburb_rank.sort_values('TotalRank').reset_index(drop=True)

    # Load the parks data from the data folder
    parks_reserves_data = pd.read_csv(os.path.join(data_dir, 'Green_parks_merge.csv'))

    # Aggregate the number of parks and total park area per suburb
    parks_summary = parks_reserves_data.groupby('suburb').agg(
        NumberOfParks=('name', 'nunique'),  # Unique parks
        TotalParkArea=('area', 'sum')  # Total park area
    ).reset_index()

    # Rank the suburbs based on parks
    parks_summary['Rank_NumberOfParks'] = parks_summary['NumberOfParks'].rank(ascending=False, method='min')  # More parks -> higher rank
    parks_summary['Rank_TotalParkArea'] = parks_summary['TotalParkArea'].rank(ascending=False, method='min')  # Larger park area -> higher rank

    # Combine the ranks into an overall parks rank
    parks_summary['OverallParksRank'] = (parks_summary['Rank_NumberOfParks'] + parks_summary['Rank_TotalParkArea']) / 2

    # Merge the parks rank with the main suburb ranking data
    suburb_rank = suburb_rank.merge(parks_summary, left_on='Suburb', right_on='suburb', how='left')

    # If user prefers parks, adjust the total rank by combining with the parks rank
    if user_input['prefer_parks']:
        suburb_rank['TotalRank'] += suburb_rank['OverallParksRank']

    # Sort suburbs by the new total rank
    suburb_rank = suburb_rank.sort_values('TotalRank').reset_index(drop=True)

    # Select the top 5 suburbs based on total rank
    top_5_suburbs = suburb_rank.head(5)
    print(top_5_suburbs)

    # Load the shapefile from the GDA2020 folder in the data directory
    shapefile_path = os.path.join(data_dir, 'GDA2020/vic_localities.shp')
    vic_localities_sf = gpd.read_file(shapefile_path)

    # Ensure that the shapefile has the correct CRS (Coordinate Reference System) in WGS84 (EPSG:4326)
    if vic_localities_sf.crs != "EPSG:4326":
        vic_localities_sf = vic_localities_sf.to_crs("EPSG:4326")

    # Preview the shapefile data
    print(vic_localities_sf.head())

    # Ensure both columns are uppercase and stripped of leading/trailing spaces
    vic_localities_sf['LOC_NAME'] = vic_localities_sf['LOC_NAME'].str.upper().str.strip()

    # Use .loc to avoid the SettingWithCopyWarning
    top_5_suburbs.loc[:, 'Suburb'] = top_5_suburbs['Suburb'].str.upper().str.strip()

    # Get the list of cleaned suburb names
    top_suburb_names = top_5_suburbs['Suburb'].tolist()

    # Filter the shapefile GeoDataFrame to include only the top 5 suburbs
    filtered_vic_localities_sf = vic_localities_sf[vic_localities_sf['LOC_NAME'].isin(top_suburb_names)]

    # Preview the filtered GeoDataFrame
    print(filtered_vic_localities_sf)

    # Merge the ranking data from top_5_suburbs with the filtered shapefile
    # Merge based on the common suburb name ('LOC_NAME' in shapefile and 'Suburb' in rank data)
    final_geo_df = filtered_vic_localities_sf.merge(top_5_suburbs, left_on='LOC_NAME', right_on='Suburb')

    # Drop the 'Suburb' column from the ranking DataFrame (since 'LOC_NAME' represents the same data)
    final_geo_df = final_geo_df.drop(columns=['Suburb'])

    # Preview the merged data to ensure that rank information is included
    print(final_geo_df.head())

    output_geoJSON_path = os.path.join(geojson_dir, 'top_5_suburbs_with_ranks.geojson')

    # Save the GeoDataFrame as GeoJSON
    final_geo_df.to_file(output_geoJSON_path, driver='GeoJSON')

    # Confirm the export was successful
    print(f"GeoJSON file created at: {output_geoJSON_path}")

    return os.path.join("geoJSON", "top_5_suburbs_with_ranks.geojson")   # Return the GeoJSON path