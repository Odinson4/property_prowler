import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the sales search page
search_url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=2'

# Send an HTTP GET request to the sales search page
search_response = requests.get(search_url)

# Check if the request was successful
if search_response.status_code == 200:
    # Parse the HTML content of the search page using BeautifulSoup
    search_soup = BeautifulSoup(search_response.text, 'html.parser')

    # Find the <a> tag with the text "Details" (assuming this is how you access the detail page)
    details_link = search_soup.find('a', string='Details')


    if details_link:
        # Extract the href attribute from the <a> tag
        detail_url = details_link.get('href')

        # Construct the full URL for the sales listing detail page
        full_detail_url = f'https://salesweb.civilview.com{detail_url}'

        # Send an HTTP GET request to the sales listing detail page
        response = requests.get(full_detail_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the detail page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the Sheriff Number if it exists, or set it to a default value if not found
            sheriff_element = soup.find('span', {'id': 'SheriffNo'})
            sheriff_number = sheriff_element.text.strip() if sheriff_element else 'N/A'

            # Extract the Court Case Number if it exists, or set it to a default value if not found
            court_case_element = soup.find('span', {'id': 'CourtCaseNo'})
            court_case_number = court_case_element.text.strip() if court_case_element else 'N/A'

            # Extract the Sales Date if it exists, or set it to a default value if not found
            sales_date_element = soup.find('span', {'id': 'SalesDate'})
            sales_date = sales_date_element.text.strip() if sales_date_element else 'N/A'

            # Extract the Plaintiff if it exists, or set it to a default value if not found
            plaintiff_element = soup.find('span', {'id': 'Plaintiff'})
            plaintiff = plaintiff_element.text.strip() if plaintiff_element else 'N/A'

            # Extract the Defendant if it exists, or set it to a default value if not found
            defendant_element = soup.find('span', {'id': 'Defendant'})
            defendant = defendant_element.text.strip() if defendant_element else 'N/A'

            # Extract the Address if it exists, or set it to a default value if not found
            address_element = soup.find('span', {'id': 'Address'})
            address = address_element.text.strip() if address_element else 'N/A'

            # Extract the Description if it exists, or set it to a default value if not found
            description_element = soup.find('span', {'id': 'Description'})
            description = description_element.text.strip() if description_element else 'N/A'

            # Extract the Approximate Upset if it exists, or set it to a default value if not found
            approx_upset_element = soup.find('span', {'id': 'ApproxUpset'})
            approximate_upset = approx_upset_element.text.strip() if approx_upset_element else 'N/A'

            # Extract the Attorney if it exists, or set it to a default value if not found
            attorney_element = soup.find('span', {'id': 'Attorney'})
            attorney = attorney_element.text.strip() if attorney_element else 'N/A'

            # Extract the Attorney Phone if it exists, or set it to a default value if not found
            attorney_phone_element = soup.find('span', {'id': 'AttorneyPhone'})
            attorney_phone = attorney_phone_element.text.strip() if attorney_phone_element else 'N/A'


            # Create a dictionary to store the extracted data
            data = {
                'Sheriff #': [sheriff_number],
                'Court Case #': [court_case_number],
                'Sales Date': [sales_date],
                'Plaintiff': [plaintiff],
                'Defendant': [defendant],
                'Address': [address],
                'Description': [description],
                'Approx. Upset': [approximate_upset],
                'Attorney': [attorney],
                'Attorney Phone': [attorney_phone]
            }

            # Create a DataFrame from the data
            df = pd.DataFrame(data)

            # Save the DataFrame to a CSV file
            df.to_csv('sales_listing.csv', index=False)

            print('Data has been successfully scraped and saved to sales_listing.csv.')
        else:
            print('Failed to retrieve the detail page. Status code:', response.status_code)
    else:
        print('Details link not found on the search page.')
else:
    print('Failed to retrieve the search page. Status code:', search_response.status_code)
