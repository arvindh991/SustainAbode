import os
import pandas as pd
import geopandas as gpd
from django.conf import settings
from io import BytesIO  # For in-memory file handling
from azure.storage.blob import BlobServiceClient
import os
from datetime import datetime  # For generating timestamps

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

    # Load the bus stop and train car park datasets
    bus_stop_data = pd.read_csv(os.path.join(data_dir, 'ptv_metro_bus_stop_cleaned.csv'))
    train_carpark_data = pd.read_csv(os.path.join(data_dir, 'ptv_train_carpark_cleaned.csv'))

    # Example: Displaying first few rows to understand the structure
    # print(bus_stop_data.head())
    # print(train_carpark_data.head())

    # Aggregate bus data by suburb
    bus_service_summary = bus_stop_data.groupby('suburb').agg(
        NumberOfBusStops=('stop_id', 'size'),  # Number of bus stops
        UniqueBusRoutes=('routes_using_stop', lambda x: len(set(",".join(x).split(','))))  # Count of unique bus routes
    ).reset_index()

    # Merge bus data with the existing suburb rankings
    suburb_rank = suburb_rank.merge(bus_service_summary, left_on='Suburb', right_on='suburb', how='left')

    # Replace missing values with 0 for suburbs with no bus service
    suburb_rank['NumberOfBusStops'].fillna(0, inplace=True)
    suburb_rank['UniqueBusRoutes'].fillna(0, inplace=True)

    # Assuming train_carpark_data contains 'suburb' and 'carpark_capacity' columns

    # Aggregate train car park data by suburb (if needed)
    carpark_summary = train_carpark_data.groupby('suburb').agg(
        TotalCarparkCapacity=('commuter_capacity', 'sum')  # Total car park capacity in the suburb
    ).reset_index()

    # Merge car park data with the suburb ranking
    suburb_rank = suburb_rank.merge(carpark_summary, left_on='Suburb', right_on='suburb', how='left')

    # Replace missing values with 0 for suburbs with no train car parks
    suburb_rank['TotalCarparkCapacity'].fillna(0, inplace=True)

    # Rank suburbs based on bus services
    suburb_rank['Rank_BusStops'] = suburb_rank['NumberOfBusStops'].rank(ascending=False, method='min')
    suburb_rank['Rank_BusRoutes'] = suburb_rank['UniqueBusRoutes'].rank(ascending=False, method='min')

    # Rank suburbs based on train car park capacity
    suburb_rank['Rank_CarparkCapacity'] = suburb_rank['TotalCarparkCapacity'].rank(ascending=False, method='min')

    # Adjust TotalRank if the user prefers bus travel
    if user_input['prefer_bus']:
        suburb_rank['TotalRank'] += (suburb_rank['Rank_BusStops'] + suburb_rank['Rank_BusRoutes'])

    # Adjust TotalRank if the user prefers train car parks
    if user_input['prefer_carpark']:
        suburb_rank['TotalRank'] += suburb_rank['Rank_CarparkCapacity']
        
    # Recompute the TotalRank based on user preferences
    suburb_rank = suburb_rank.sort_values('TotalRank').reset_index(drop=True)

    # Select the top 5 suburbs based on total rank
    top_5_suburbs = suburb_rank.head(5)
    # print(top_5_suburbs)

    # Select the top 5 suburbs based on total rank and explicitly create a copy
    top_5_suburbs = suburb_rank.head(5).copy()

    # Add a 'SerialNumber' column with values 1 through 5
    top_5_suburbs['SerialNumber'] = range(1, len(top_5_suburbs) + 1)

    # Preview the top 5 suburbs with the serial number
    # print(top_5_suburbs[['Suburb', 'TotalRank', 'SerialNumber']])

    # Load the shapefile from the GDA2020 folder in the data directory
    shapefile_path = os.path.join(data_dir, 'GDA2020/vic_localities.shp')
    vic_localities_sf = gpd.read_file(shapefile_path)

    # Ensure that the shapefile has the correct CRS (Coordinate Reference System) in WGS84 (EPSG:4326)
    if vic_localities_sf.crs != "EPSG:4326":
        vic_localities_sf = vic_localities_sf.to_crs("EPSG:4326")

    # Preview the shapefile data
    # print(vic_localities_sf.head())

    # Ensure both columns are uppercase and stripped of leading/trailing spaces
    vic_localities_sf['LOC_NAME'] = vic_localities_sf['LOC_NAME'].str.upper().str.strip()

    # Use .loc to avoid the SettingWithCopyWarning
    top_5_suburbs.loc[:, 'Suburb'] = top_5_suburbs['Suburb'].str.upper().str.strip()

    # Get the list of cleaned suburb names
    top_suburb_names = top_5_suburbs['Suburb'].tolist()

    # Filter the shapefile GeoDataFrame to include only the top 5 suburbs
    filtered_vic_localities_sf = vic_localities_sf[vic_localities_sf['LOC_NAME'].isin(top_suburb_names)]

    # Preview the filtered GeoDataFrame
    # print(filtered_vic_localities_sf)

    # Merge the ranking data from top_5_suburbs with the filtered shapefile
    # Merge based on the common suburb name ('LOC_NAME' in shapefile and 'Suburb' in rank data)
    final_geo_df = filtered_vic_localities_sf.merge(top_5_suburbs, left_on='LOC_NAME', right_on='Suburb')

    # Drop the 'Suburb' column from the ranking DataFrame (since 'LOC_NAME' represents the same data)
    final_geo_df = final_geo_df.drop(columns=['Suburb'])    

    # Preview the merged data to ensure that rank information is included
    # print(final_geo_df.head())

    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create a unique blob name by appending the timestamp
    blob_name = f'top_5_suburbs_with_ranks_{timestamp}.geojson'

    # Connect to the Blob service
    blob_service_client = BlobServiceClient(account_url=settings.AZURE_ACCOUNT_URL, credential=settings.AZURE_ACCOUNT_KEY)
    
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER, blob=blob_name)

    # Write the GeoDataFrame to a bytes buffer (in-memory) as GeoJSON
    geojson_buffer = BytesIO()
    final_geo_df.to_file(geojson_buffer, driver='GeoJSON')
    
    # Move the buffer's position to the start before reading (necessary to upload)
    geojson_buffer.seek(0)

    blob_url = f"{settings.AZURE_CONTAINER_URL}/{blob_name}"

    try:
        # Upload the in-memory GeoJSON data to the Blob
        blob_client.upload_blob(geojson_buffer, overwrite=True)
        # print(f"GeoJSON uploaded successfully to {blob_url}")
    except Exception as e:
        print(f"Error uploading GeoJSON to Blob: {str(e)}")
        raise

    return blob_url, top_suburb_names   # Return the GeoJSON path