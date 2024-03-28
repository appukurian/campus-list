import json

# Load the JSON data from the file
with open('updated_colleges.json', 'r') as file:
    colleges = json.load(file)

# Aggregate the data to count colleges in each category
category_counts = {}
for college in colleges:
    category = college['category']
    if category not in category_counts:
        category_counts[category] = 0
    category_counts[category] += 1

# Prepare the list of categories and their college counts
category_list = [{"Category": category, "Number of Colleges": count} for category, count in category_counts.items()]

# Display or use the category list as needed
for category_info in category_list:
    print(category_info)

