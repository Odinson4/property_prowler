import pandas as pd
import requests
import time  # Import the time module

def fetch_redfin_data(address):
    url = "https://redfin5.p.rapidapi.com/properties/get-info"

    headers = {
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
        "X-RapidAPI-Host": "redfin5.p.rapidapi.com"
    }

    querystring = {
        "url": address
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data for address: {address}. Status code: {response.status_code}")
        return None

if __name__ == '__main__':
    # Load the CSV file with addresses
    df = pd.read_csv('sales_listing.csv')

    # Initialize a list to store Redfin data
    redfin_data = []

    for index, row in df.iterrows():
        address = row['Address:']  # Extract the address from the DataFrame

        print(f'Fetching Redfin data for address: {address}')

        # Call the fetch_redfin_data function with the address as an argument
        data = fetch_redfin_data(address)

        if data:
            redfin_data.append(data)

        # Introduce a delay of a few seconds (you can adjust the duration as needed)
        time.sleep(5)  # Wait for 5 seconds between requests

    # Create a DataFrame from the Redfin data
    redfin_df = pd.DataFrame(redfin_data)

    # Merge the Redfin data with the original DataFrame based on the 'Address' column
    merged_df = df.merge(redfin_df, on='Address:', how='left')

    # Save the updated DataFrame to a new CSV file
    merged_df.to_csv('sales_listing_with_redfin.csv', index=False)

    print("Redfin data retrieval complete.")
