import requests
from bs4 import BeautifulSoup
import json

# Base URL of the website to scrape
base_url = "https://www.thrissurkerala.com/keralacollegedetails.aspx?slno="

# List to store the collected college data
colleges = []

# Iterate through the range of slno values
for slno in range(1, 2307):
    # Construct the URL for the current college
    url = f"{base_url}{slno}"

    # Fetch the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the required data from the page
    college_name = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
    details = soup.find_all('p')  # Assuming details are in <p> tags, modify as needed

    # Example extraction, modify selectors based on actual HTML structure
    address = details[0].text.strip() if len(details) > 0 else 'N/A'
    university = details[1].text.strip() if len(details) > 1 else 'N/A'
    district = details[2].text.strip() if len(details) > 2 else 'N/A'
    category = details[3].text.strip() if len(details) > 3 else 'N/A'
    college_type = details[4].text.strip() if len(details) > 4 else 'N/A'

    # Store the data in a dictionary
    college_data = {
        'slno': slno,
        'name': college_name,
        'address': address,
        'university': university,
        'district': district,
        'category': category,
        'type': college_type
    }

    # Append the college data to the list
    colleges.append(college_data)

    # Print progress
    print(f"Processed {slno}/{2306}")

# Convert the list to JSON
json_data = json.dumps(colleges, indent=4)

# Save the JSON data to a file
with open('colleges.json', 'w') as f:
    f.write(json_data)

print("Data scraping completed and saved to colleges.json")
