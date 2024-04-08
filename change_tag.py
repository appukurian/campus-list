import json
import csv
from collections import OrderedDict

# Load the existing JSON data
with open('final_updated_colleges.json', 'r') as json_file:
    colleges_data = json.load(json_file, object_pairs_hook=OrderedDict)

# Update the JSON structure, moving 'campus_name' to the beginning
updated_colleges_data = []
for college in colleges_data:
    # Ensure 'name' is changed to 'campus_name' and is the first key
    updated_college = OrderedDict([('campus_name', college.pop('name'))])
    updated_college.update(college)
    updated_colleges_data.append(updated_college)

# Write the updated data to a CSV file
csv_file_path = 'updated_colleges.csv'
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=updated_colleges_data[0].keys())
    writer.writeheader()
    writer.writerows(updated_colleges_data)

print(f"Updated JSON data exported to CSV file at {csv_file_path}")
