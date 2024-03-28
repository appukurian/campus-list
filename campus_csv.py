import json
import csv

# Load the JSON data from the file
with open('updated_colleges_with_location.json', 'r', encoding='utf-8') as file:
    colleges = json.load(file)

# Open a CSV file to write the data, ensuring UTF-8 encoding and Unix-style line endings
with open('colleges_location_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['SL No', 'Name', 'Location Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # Iterate over each college and write the relevant data to the CSV file
    for college in colleges:
        writer.writerow({
            'SL No': college['slno'],
            'Name': college['name'],
            'Location Link': college['location']
        })

print("CSV file created successfully.")
