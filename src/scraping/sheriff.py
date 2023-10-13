import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the base URL
base_url = 'https://salesweb.civilview.com/'

# Define the URL of the sales search page
search_url = f'{base_url}Sales/SalesSearch?countyId=2'

# Create a session to maintain state
session = requests.Session()

# Send an HTTP GET request to the search page
response = session.get(search_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the search page using BeautifulSoup
    search_soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the <a> tags with the text "Details" to extract the detail URLs
    details_links = search_soup.find_all('a', string='Details')

    if details_links:
        # Initialize an empty list to store the scraped data
        scraped_data = []

        for details_link in details_links:
            # Initialize a dictionary to store data for each detail page
            data = {}

            # Extract the href attribute from the <a> tag to get the detail URL
            detail_url = f'{base_url}{details_link.get("href")}'

            # Send an HTTP GET request to the sales detail page using the session
            response = session.get(detail_url)

            print('Detail URL:', detail_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the detail page using BeautifulSoup
                detail_soup = BeautifulSoup(response.text, 'html.parser')

                # Helper function to extract text from an element or return 'N/A' if not found
                def extract_text(element):
                    return element.get_text(strip=True) if element else 'N/A'

                # Find all the rows in the table
                rows = detail_soup.find_all('tr')

                # Iterate through the rows and extract data based on the labels
                for row in rows:
                    # Extract the text from the first column (label)
                    label = extract_text(row.find('td', class_='heading-bold columnwidth-15'))

                    # Find the second <td> element within the current row containing data
                    value_element = row.find_all('td')[1] if len(row.find_all('td')) > 1 else None

                    # Extract the text from the second <td> element
                    value = extract_text(value_element)

                    print(f'{label}: {value}')

                    # Add the data to the dictionary
                    data[label] = value

                # Append the data dictionary to the scraped_data list
                scraped_data.append(data)

                print('Data extracted:', data)

            else:
                print(f'Failed to retrieve the detail page for URL: {detail_url}. Status code:', response.status_code)

        # Create a DataFrame from the scraped_data list
        df = pd.DataFrame(scraped_data)

        # Save the DataFrame to a CSV file
        df.to_csv('sales_listing.csv', index=False)

        print('Data has been successfully scraped and saved to sales_listing.csv.')
    else:
        print('Details links not found on the search page.')
else:
    print(f'Failed to retrieve the search page. Status code:', response.status_code)
