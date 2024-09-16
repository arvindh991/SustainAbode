import os
import matplotlib
# Set the backend to 'Agg' to prevent any GUI from being used
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from django.conf import settings
import pandas as pd

# Function to check if a blob exists in Azure Blob Storage
def check_if_blob_exists(blob_name):
    blob_service_client = BlobServiceClient(account_url=settings.AZURE_ACCOUNT_URL, credential=settings.AZURE_ACCOUNT_KEY)
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER, blob=blob_name)

    try:
        blob_client.get_blob_properties()
        return True  # Blob exists
    except:
        return False  # Blob doesn't exist

# Function to save report to Azure Blob Storage if it doesn't exist
def save_report_to_blob(report_image, suburb_name, report_type):
    blob_name = f'{report_type}_{suburb_name}.png'  # Remove timestamp from blob name for uniqueness per suburb and report type

    # Check if the blob already exists
    if check_if_blob_exists(blob_name):
        return f"{settings.AZURE_CONTAINER_URL}/{blob_name}"  # Return existing blob URL

    # If the blob does not exist, upload the new report
    blob_service_client = BlobServiceClient(account_url=settings.AZURE_ACCOUNT_URL, credential=settings.AZURE_ACCOUNT_KEY)
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER, blob=blob_name)

    try:
        # Upload the image to the blob storage
        blob_client.upload_blob(report_image, overwrite=False)
    except Exception as e:
        raise Exception(f"Error uploading {report_type} to Blob: {str(e)}")

    return f"{settings.AZURE_CONTAINER_URL}/{blob_name}"  # Return new blob URL

def generate_score_breakdown(suburb_data):
    # Extract the individual ranks contributing to the total score
    house_count_score = suburb_data['Rank_HouseCount']
    price_score = suburb_data['Rank_AveragePrice']
    distance_score = suburb_data['Rank_AverageDistance']
    bus_score = suburb_data['Rank_BusStops'] + suburb_data['Rank_BusRoutes']
    carpark_score = suburb_data['Rank_CarparkCapacity']
    parks_score = suburb_data['OverallParksRank'] if 'OverallParksRank' in suburb_data else 0  # Optional

    # Combine all scores into a dictionary for display
    score_breakdown = {
        'House Count': house_count_score,
        'Average Price': price_score,
        'Proximity': distance_score,
        'Bus Services': bus_score,
        'Car Park Capacity': carpark_score,
        'Parks': parks_score
    }

    # Handle any NaN values by replacing them with 0
    score_breakdown = {k: (0 if pd.isna(v) else v) for k, v in score_breakdown.items()}

    # Normalize the scores so that they sum to the total score
    total_score = sum(score_breakdown.values())
    
    # Avoid division by zero in case the total score is 0
    if total_score == 0:
        normalized_scores = {k: 0 for k in score_breakdown.keys()}
    else:
        normalized_scores = {k: (v / total_score) * 100 for k, v in score_breakdown.items()}

    # Return the breakdown and normalized scores
    return score_breakdown, normalized_scores


def generate_piechart_image(suburb_name, geo_df):
    # Generate the pie chart and save to an in-memory buffer
    selected_suburb_data = geo_df[geo_df['LOC_NAME'] == suburb_name.upper()].iloc[0]
    score_breakdown, normalized_scores = generate_score_breakdown(selected_suburb_data)

    labels_mapping = {
        'House Count': 'Available houses within price range',
        'Average Price': 'Percentage of affordable houses',
        'Proximity': 'How far from the Central Business District',
        'Bus Services': 'Popularity of public transportation',
        'Car Park Capacity': 'Car parking availability',
        'Parks': 'Nearby parks availability'
    }

    labels = [labels_mapping.get(label, label) for label in normalized_scores.keys()]
    sizes = list(normalized_scores.values())

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
    ax.set_title(f'Factors contributing to the overall rank of {suburb_name}', fontsize=16)

    plt.tight_layout()  # Ensure the layout fits well

    # Save to an in-memory buffer (DO NOT SHOW THE PLOT)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)  # Close the figure to prevent it from showing

    return buffer.getvalue()  # Return the image buffer data


def generate_price_distribution_image(suburb_name, melbourne_data):
    # Generate the price distribution histogram and save to an in-memory buffer
    suburb_data = melbourne_data[melbourne_data['Suburb'].str.upper() == suburb_name.upper()]['Price'].dropna()

    if suburb_data.empty:
        print(f"No data available for suburb '{suburb_name}'.")
        return None  # Handle case if no data is available
    
    average_price = suburb_data.mean()

    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(suburb_data, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    
    # Normalize the bin counts for color scaling
    norm_counts = counts / counts.max()
    
    # Apply color to each bar based on the count (higher count -> darker color)
    for count, patch in zip(norm_counts, patches):
        plt.setp(patch, 'facecolor', plt.cm.Blues(count))
    
    # Add a vertical line for the average price
    ax.axvline(average_price, color='red', linestyle='dashed', linewidth=2)
    
    # Label the average price on the line
    ax.text(average_price * 1.02, ax.get_ylim()[1] * 0.9, f'Average Price: ${int(average_price):,}', color='red')
    
    # Set the title and labels
    ax.set_title(f'House Price Distribution in {suburb_name}', fontsize=16)
    ax.set_xlabel('Price (in $)', fontsize=14)
    ax.set_ylabel('Number of Houses', fontsize=14)

    # Format the x-axis to show values in $K and $M
    def price_format(x, _):
        if x >= 1e6:
            return f'${x / 1e6:.2f}M'
        else:
            return f'${x / 1e3:.0f}K'

    ax.xaxis.set_major_formatter(plt.FuncFormatter(price_format))

    plt.tight_layout()  # Adjust layout

    # Save to an in-memory buffer (DO NOT SHOW THE PLOT)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)  # Close the figure to prevent it from showing

    return buffer.getvalue()

# Function to generate and save reports for a given suburb
def generate_and_save_reports_for_suburb(suburb_name, geo_df, melbourne_data):
    report_urls = {}

    # Pie chart report
    piechart_image = generate_piechart_image(suburb_name, geo_df)
    piechart_url = save_report_to_blob(piechart_image, suburb_name, 'piechart')
    report_urls['piechart'] = piechart_url

    # House price distribution report (histogram)
    histogram_image = generate_price_distribution_image(suburb_name, melbourne_data)
    histogram_url = save_report_to_blob(histogram_image, suburb_name, 'price_distribution')
    report_urls['price_distribution'] = histogram_url

    # Add other reports as needed following the same pattern

    return report_urls
