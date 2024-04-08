import json

# Load the JSON data from the file
with open('updated_colleges_with_polytechnic_names.json', 'r') as json_file:
    colleges_data = json.load(json_file)

# Use a dictionary to track unique colleges and a set for duplicate names
unique_colleges = {}
duplicates = set()

for college in colleges_data:
    campus_name = college['campus_name']
    if campus_name in unique_colleges:
        duplicates.add(campus_name)
    else:
        unique_colleges[campus_name] = college

# Get the list of unique colleges from the dictionary
cleaned_colleges = list(unique_colleges.values())

# Save the cleaned data to a new JSON file
with open('cleaned_colleges.json', 'w') as json_file:
    json.dump(cleaned_colleges, json_file, indent=4)

# Print the duplicate campus names
print("Duplicate campus names:")
for name in duplicates:
    print(name)

