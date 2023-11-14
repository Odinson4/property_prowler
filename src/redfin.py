import pandas as pd
import requests
from bs4 import BeautifulSoup

# Read the CSV file containing addresses
csv_file = 'sales_listing.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Function to get property value from Trulia
def get_property_value(address):
    trulia_url = f"https://www.trulia.com/{address.replace(' ', '-')}"
    print(f"Processing address: {address}")
    response = requests.get(trulia_url)
    
    if response.status_code == 200:
        print(f"Successfully fetched data for address: {address}")
        soup = BeautifulSoup(response.text, 'html.parser')
        # Be more precise in selecting the element
        property_value_div = soup.find('div', {'class': 'Text__TextBase-sc-27a633b1-0-div Text__TextContainerBase-sc-27a633b1-1 jrMHya gtvmjT'})
        print(property_value_div)
        
        if property_value_div:
            property_value = property_value_div.text.strip()
            print(f"Property value found for address: {address} - Value: {property_value}")
            return property_value
        else:
            print(f"Property value not found for address: {address}")
    else:
        print(f"Failed to fetch data for address: {address}")

    return 'Not found'

# Create a new column for property values in the DataFrame
df['Property_Value'] = df['Address:'].apply(get_property_value)

# Save the updated DataFrame to a new CSV file
output_csv_file = 'property_values.csv'
df.to_csv(output_csv_file, index=False)

print(f"Property values saved to {output_csv_file}")
