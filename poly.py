import json

# List of college names and addresses
colleges_data = [
    "Model Residential Polytechnic College, Kuzhalmannam, Palakkad",
    "Kuttukaran Polytechnic College, North Parvur, Ernakulam",
    "Kerala Government Polytechnic College, Westhill P.O, Kozhikode",
    "Government Polytechnic College, Nattakom P.O., Kottayam, 686013",
    "Central Polytechnic, Vattiyoorkavu P.O, Thiruvananthapuram, 695013",
    "Maharaja's Technological Institute, Chembukavu, Thrissur 680020",
    "AWH Polytechnic College, Kuttikkattoor, Kozhikode",
    "Carmel Polytechnic, Punnapra P.O., Alappuzha, 688004",
    "Government Polytechnic, Angadippuram, Perinthalmanna, 679321",
    "Government Polytechnic, Attingal, 695101",
    "Government Polytechnic, Ezhukone, Kollam",
    "Government Polytechnic, Kalamassery, 683104",
    "Government Polytechnic, Koovappady P.O., Perumbavoor, Ernakulam",
    "Government Polytechnic, Koratty",
    "Government Polytechnic, Kothamangalam, Chelad P.O., 686681, Ernakulam",
    "Government Polytechnic, Kumily",
    "Government Polytechnic, Kunnamkulam, Kizhoor P.O., Trichur, 680523",
    "Government Polytechnic College, Karuvambram P.O, Manjeri, Kerala 676517",
    "Government Polytechnic, Manakala P.O., Adoor, Pathanamthitta, 691523",
    "Government Polytechnic, Marothrvattom P.O., Cherthala, Alappuzha, 688545",
    "Government Polytechnic, Mattannur, Kannur, 670 702",
    "Government Polytechnic, Meppadi, Wayanad, 673577",
    "Government Polytechnic, Meenangadi, Wayanad, 673591",
    "Government Polytechnic, Muttom P.O., Thodupuzha, Idukki, 685587",
    "Government Polytechnic, Nedumangad",
    "Government Polytechnic, Nedumkandam",
    "Government Polytechnic, P.O. Periye, Kasaragod, 671316",
    "Government Polytechnic College, Pala, Kottayam Dist., 686575",
    "Government Polytechnic, Punalur",
    "Government Polytechnic, Perumpazhuthoor, Thiruvananthapuram",
    "Government Polytechnic, Purappuzha P.O., Thodupuzha, Idukki, 685583",
    "Government Polytechnic, Thottada",
    "Government Polytechnic, Thrikaripur",
    "Government Polytechnic, Vennikulam, Pathanamthitta, 589544",
    "Government Polytechnic College, Chelakkara, Thrissur",
    "Government Polytechnic College, Thirurangadi, Velimukku P.O., Malappuram, 676317",
    "Government Women's Polytechnic, Kaimonom, Thiruvananthapuram",
    "Orphanage Polytechnic College, Edavanna",
    "Institute of Printing Technology & Government Polytechnic College, Kulappully, Shoranur, 679122, Palakkad",
    "J.D.T Islam Polytechnic, P.B. No. 1702, Marikkunnu, Kozhikode, 673012",
    "KELTRON TOOLROOM RESEARCH AND TRAINING CENTRE, Keltron complex, Keltron road, Aroor, Alappuzha-688534",
    "KMCT Polytechnic College, Kalananthode Chanthamangalam, Kozhikode",
    "Ma'din Polytechnic College, Melmuri, Malappuram",
    "Model Polytechnic, Kallettumkara P.O., Thrissur, 680683",
    "Model Polytechnic, Mattakkara, P.O Kottayam, 686564",
    "Model Polytechnic, Nut Street, Vatakara, 673104, Kozhikode",
    "Model Polytechnic, Painavu, Idukki District",
    "N.S.S. Polytechnic, Mannamnagar P.O., Pandalam, 689501",
    "Residential Women's Polytechnic, Payyanur, Kannur, 670307",
    "S.N.Polytechnic, Kanhangad, Kasaragod, 671315",
    "Seethi Sahib Memorial Polytechnic, P.B. No.1, P.O Thekkummuri, Tirur, 676105",
    "S.N.Polytechnic, Kottiyam, Kollam, 691 571",
    "Sree Rama Polytechnic, Valapad, Thrissur, 680567",
    "St. Mary's Polytechnic College, Valliyode, Palakkad",
    "Thiagarajar Polytechnic College, Alagappanagar P.O., 680302, Thrissur",
    "Women's Polytechnic, Ernakulam, Kalamassery P.O.",
    "Women's Polytechnic, Kayamkulam",
    "Women's Polytechnic, Kottakkal, P.O. Valavannur, Malappuram",
    "Women's Polytechnic, Kozhikode, 673009",
    "Women's Polytechnic, Nedupuzha P.O., Thrissur, 680015"
]

# Initialize the list for JSON data
colleges_json = []
slno = 1219

for college in colleges_data:
    # Splitting the address to get the district
    parts = college.split(',')
    name = parts[0].strip()
    address = college.strip()
    district = parts[-1].strip() if len(parts) > 1 else 'Unknown'

    # Create Google Maps search link
    search_query = address.replace(' ', '+')
    location = f"https://www.google.com/maps/search/?api=1&query={search_query}"

    # Create the college JSON object
    college_json = {
        "slno": slno,
        "name": name,
        "address": address,
        "university": "Unknown",  # University information is not provided
        "district": district,
        "category": "Polytechnic College",
        "type": "Unknown",  # Type information is not provided
        "location": location
    }
    colleges_json.append(college_json)
    slno += 1

# Convert the list to JSON
json_data = json.dumps(colleges_json, indent=4)

# Save the JSON data to a file
with open('polytechnic_colleges.json', 'w') as f:
    f.write(json_data)
