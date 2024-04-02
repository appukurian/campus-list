import json

# Define the list of target colleges
target_colleges = [
    "College of Engineering, Kidangoor",
    "MES College, Marampally",
    "KMEA Engineering College, Edathala",
    "Rajadhani Institute of Engineering and Technology, Attingal",
    "Model Engineering College, Thrikkakara",
    "Rajiv Gandhi Institute Of Technology, Kottayam",
    "Toc H Institute of Science and Technology, Arakunnam",
    "Cochin University College of Engineering, Kuttanad",
    "Govt. Engineering College, Sreekrishnapuram, Palakkad",
    "KMCT College of Engineering, Kallanthode",
    "MES College Of Engineering, Kuttippuram",
    "College of Engineering, Trivandrum",
    "NSS College Of Engineering, Palakkad",
    "College Of Engineering, Chengannur",
    "Adi Shankara Institute of Engineering and Technology, Kalady",
    "School Of Engineering CUSAT, Kalamassery",
    "Institute Of Engineering And Technology CALICUT UNIVERSITY, Kohinoor",
    "Safi Institute of Advanced Study, Vazhayur",
    "Government Engineering College, Thrissur",
    "Christ College of Engineering, Irinjalakuda",
    "Albertian Institute Of Science And Technology, Kalamassery",
    "EMEA Arts & Science College, Kondotty",
    "Farook College(Autonomous), Kozhikode",
    "College Of Engineering, Karunagappally",
    "Sree Buddha College of Engineering, Pattoor, Alappuzha",
    "Jyothi Engineering College, Thrissur",
    "College of Engineering, Cherthala",
    "Mohammed Abdurahiman Memorial Orphanage College, Manassery",
    "M Dasan Institute of Technology Ulliyeri, Kozhikode",
    "Sullamussalam Science College, Areekode",
    "Marian Engineering College, Trivandrum",
    "Government College of Engineering, Kannur",
    "Carmel College of Engineering and Technology, Alappuzha",
    "College of Engineering, Vadakara",
    "Government Engineering College, Wayanad",
    "Mar Baselios Christian College of Engineering & Technology, Kuttikkanam",
    "College of Engineering, Aranmula",
    "St. Joseph's College of Engineering and Technology, Palai",
    "LBS College of Engineering, Kasaragod",
    "Majlis Arts and Science College, Malappuram",
    "LBS Institute of Technology for Women, Poojappura",
    "College of Engineering and Management, Punnapra",
    "Mar Athanasius College of Engineering, Kothamangalam",
    "Ilahia College of Engineering and Technology, Muvattupuzha",
    "College of Engineering, Munnar",
    "Muthoot Institute of Technology and Science, Kochi",
    "Saintgits College of Engineering, Pathamuttom",
    "TKM College of Engineering, Kollam",
    "SCMS School of Engineering and Technology, Karukutty",
    "Department of Computer Science, CUSAT, Kochi",
    "Jai Bharath College of Management & Engineering Technology",
    "University College of Engineering, Kariavattom",
    "Yeldo Mar Baselios College, Kothamangalam",
    "Sree Narayana Gurukulam College Of Engineering, Ernakulam",
    "Musaliar College of Engineering & Technology, Pathanamthitta",
    "Seethi Sahib Memorial Polytechnic College, Tirur",
    "Rajagiri School of Engineering and Technology, Ernamkulam"
]


# Load the existing JSON data
with open('updated_colleges_with_th_campus.json', 'r') as json_file:
    colleges_data = json.load(json_file)

# Track colleges not found in the JSON data
not_found_colleges = []

# Update the 'th_campus' field for matching colleges and track not found colleges
for target in target_colleges:
    found = False
    for college in colleges_data:
        if college['address'] == target:
            college['th_campus'] = True
            found = True
            break
    if not found:
        not_found_colleges.append(target)

# Save the updated JSON data back to a file
with open('final_updated_colleges.json', 'w') as json_file:
    json.dump(colleges_data, json_file, indent=4)

# Print the list of colleges not found in the JSON data
print("Colleges not identified in the JSON file:")
for college in not_found_colleges:
    print(college)
