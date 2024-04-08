import csv
from math import ceil

# Path to the original CSV file
original_csv_path = 'updated_colleges_polytechnic.csv'

# Read the original CSV file
with open(original_csv_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Get the header and data rows
header = rows[0]
data_rows = rows[1:]

# Determine the number of rows per file
total_rows = len(data_rows)
rows_per_file = ceil(total_rows / 10)

# Split the data and write to separate CSV files
for i in range(10):
    split_data = data_rows[i * rows_per_file:(i + 1) * rows_per_file]
    split_file_path = f'updated_colleges_polytechnic_part_{i + 1}.csv'
    with open(split_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header in each new file
        writer.writerows(split_data)

print("CSV file successfully split into 10 parts.")
