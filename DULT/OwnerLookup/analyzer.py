#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import csv

def analyze_csv(file_path):
    data = {}

    # Read the CSV file and collect values in arrays based on the time offset
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            time_offset = int(row[0])
            value = int(row[1])
            if time_offset not in data:
                data[time_offset] = []
            data[time_offset].append(value)

    # Analyze the collected data
    for time_offset, values in data.items():
        less = sum(1 for v in values if v < time_offset)
        greater_or_equal = sum(1 for v in values if v >= time_offset)
        print(f"Time Offset: {time_offset}, Less: {less}, Greater or Equal: {greater_or_equal}, Total: {len(values)}")

if __name__ == '__main__':
    # Example usage
    csv_file = 'Results/eid_scan_results.csv'
    analyze_csv(csv_file)