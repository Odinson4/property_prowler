import pandas as pd
from sheriff import scrape_sheriff_data

# Load the CSV file with addresses
df = pd.read_csv('sales_listing.csv')

# Initialize a list to store Sheriff data
sheriff_data = []

# Iterate through the DataFrame
for index, row in df.iterrows():
    address = row['Address:']  # Extract the address from the DataFrame

    print(f'Processing address: {address}')

    # Call the scrape_sheriff_data function with the address as an argument
    data = scrape_sheriff_data()

    # Append the Sheriff data to the list
    sheriff_data.append(data)

# Create a DataFrame from the Sheriff data
sheriff_df = pd.DataFrame(sheriff_data)

# Merge the Sheriff data with the original DataFrame based on the 'Address' column
merged_df = df.merge(sheriff_df, on='Address:', how='left')

# Save the updated DataFrame to a new CSV file
merged_df.to_csv('sales_listing.csv', index=False)
