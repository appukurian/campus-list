import json
import csv

# Load the existing JSON data
with open('updated_colleges_with_location.json', 'r') as json_file:
    colleges_data = json.load(json_file)

# Load the CSV data
updated_locations = {}
with open('campuslist-test.csv', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        updated_locations[int(row['slno'])] = row['new_location']

# Update the JSON data with new location links
for college in colleges_data:
    slno = college['slno']
    if slno in updated_locations:
        college['location'] = updated_locations[slno]

# Save the updated JSON data back to a file
with open('updated_colleges_with_new_locations.json', 'w') as json_file:
    json.dump(colleges_data, json_file, indent=4)

print("Updated locations in JSON data successfully.")
