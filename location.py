import json
import urllib.parse

# Load the JSON data from the file
with open('updated_colleges.json', 'r') as file:
    colleges = json.load(file)

# Iterate over each college and construct the Google Maps search URL
for college in colleges:
    # Encode the address to be URL-friendly
    encoded_address = urllib.parse.quote(college['address'])
    google_maps_search_url = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"
    
    # Add the search URL to the college data
    college['location'] = google_maps_search_url

# Save the updated data back to a JSON file
with open('updated_colleges_with_location.json', 'w') as file:
    json.dump(colleges, file, indent=4)
