import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the base URL
base_url = 'https://salesweb.civilview.com/'

# Define the URL of the sales search page
search_url = f'{base_url}Sales/SalesSearch?countyId=2'

# Send an HTTP GET request to the search page
response = requests.get(search_url)

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
            # Extract the href attribute from the <a> tag to get the detail URL
            detail_url = f'{base_url}{details_link.get("href")}'

            # Send an HTTP GET request to the sales detail page
            response = requests.get(detail_url)

            print('Detail URL:', detail_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the detail page using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Helper function to extract text from an element or return 'N/A' if not found
                def extract_text(element):
                    return element.get_text(strip=True) if element else 'N/A'

                # Find all the rows in the table
                rows = soup.find_all('tr')

                print ('rows:', rows)
                print ('len(rows):', len(rows))
                print ('rows[0]:', rows[0])

                # Initialize variables to store the scraped data for each detail page
                sheriff_number = court_case_number = sales_date = plaintiff = defendant = address = description = approximate_upset = attorney = attorney_phone = 'N/A'

                # Iterate through the rows and extract data based on the labels
                for row in rows:
                    label = row.find('td')
                    if label:
                        label_text = label.get_text(strip=True)
                        data_cell = label.find_next_sibling('td')

                        if data_cell:
                            data_text = data_cell.get_text(strip=True)
                        else:
                            data_text = 'N/A'

                        # Print the label and data for debugging
                        print(f'Label: {label_text}')
                        print(f'Data: {data_text}')

                # Create a dictionary to store the extracted data for the current detail page
                data = {
                    'Sheriff #': sheriff_number,
                    'Court Case #': court_case_number,
                    'Sales Date': sales_date,
                    'Plaintiff': plaintiff,
                    'Defendant': defendant,
                    'Address': address,
                    'Description': description,
                    'Approx. Upset': approximate_upset,
                    'Attorney': attorney,
                    'Attorney Phone': attorney_phone
                }

                print ('Data:', data)
                print ('row:', row)

                # Append the data to the scraped_data list
                scraped_data.append(data)
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
