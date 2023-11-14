import pandas as pd
from sheriff import scrape_sheriff_data
from redfin import fetch_redfin_data

# Load the CSV file with addresses
df = pd.read_csv('sales_listing.csv')

# Initialize a list to store Redfin data
redfin_data = []

# Iterate through the DataFrame
for index, row in df.iterrows():
    address = row['Address:']  # Extract the address from the DataFrame

    print(f'Fetching Redfin data for address: {address}')

    # Call the fetch_redfin_data function with the address as an argument
    data = fetch_redfin_data(address)

    # Append the Redfin data to the list
    redfin_data.append(data)

# Create a DataFrame from the Redfin data
redfin_df = pd.DataFrame(redfin_data)

# Merge the Redfin data with the original DataFrame based on the 'Address' column
merged_df = df.merge(redfin_df, on='Address:', how='left')

# Save the updated DataFrame to a new CSV file
merged_df.to_csv('sales_listing_with_redfin.csv', index=False)

print("Redfin data retrieval complete.")
