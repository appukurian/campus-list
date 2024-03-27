import json

# Load the JSON data
with open('colleges.json', 'r') as file:
    colleges = json.load(file)

# List of districts in Kerala
kerala_districts = ["Thiruvananthapuram", "Kollam", "Alappuzha", "Pathanamthitta", 
                    "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", 
                    "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"]

# Filter out colleges outside Kerala and update slno
filtered_colleges = []
for college in colleges:
    if college['district'] in kerala_districts:
        filtered_colleges.append(college)

for index, college in enumerate(filtered_colleges, start=1):
    college['slno'] = index

# Save the updated list to a new JSON file
with open('updated_colleges.json', 'w') as file:
    json.dump(filtered_colleges, file, indent=4)
