import json
import csv

# Load the JSON data from the file
with open('updated_colleges_with_polytechnic_names.json', 'r', encoding='utf-8') as file:
    colleges = json.load(file)

# Determine all unique headers from the JSON data
fieldnames = set()
for college in colleges:
    fieldnames.update(college.keys())
fieldnames = sorted(fieldnames)

# Open a CSV file to write the data, ensuring UTF-8 encoding and Unix-style line endings
with open('colleges_location_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # Iterate over each college and write the relevant data to the CSV file
    for college in colleges:
        writer.writerow(college)

print("CSV file created successfully.")
