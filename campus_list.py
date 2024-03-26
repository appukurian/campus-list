import requests
from bs4 import BeautifulSoup
import json

# Base URL of the website to scrape
base_url = "https://www.thrissurkerala.com/keralacollegedetails.aspx?slno="

# List to store the collected college data
colleges = []

# Iterate through the range of slno values
for slno in range(1, 2307):
    url = f"{base_url}{slno}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the required data from the page
    college_name_element = soup.find('span', id='ctl00_ContentPlaceHolder1_DetailsView1_Label2')
    address_element = soup.find('span', id='ctl00_ContentPlaceHolder1_DetailsView1_Label3')
    university_element = soup.find('span', id='ctl00_ContentPlaceHolder1_DetailsView1_Label8')
    district_element = soup.find('span', id='ctl00_ContentPlaceHolder1_DetailsView1_Label9')
    category_element = soup.find('span', id='ctl00_ContentPlaceHolder1_DetailsView1_Label10')
    college_type_element = soup.find('span', id='ctl00_ContentPlaceHolder1_DetailsView1_Label11')

    college_data = {
        'slno': slno,
        'name': college_name_element.text.strip() if college_name_element else 'N/A',
        'address': address_element.text.strip() if address_element else 'N/A',
        'university': university_element.text.strip() if university_element else 'N/A',
        'district': district_element.text.strip() if district_element else 'N/A',
        'category': category_element.text.strip() if category_element else 'N/A',
        'type': college_type_element.text.strip() if college_type_element else 'N/A'
    }

    colleges.append(college_data)
    print(f"Processed {slno}/{2306}")

json_data = json.dumps(colleges, indent=4)
with open('colleges.json', 'w') as f:
    f.write(json_data)

print("Data scraping completed and saved to colleges.json")
