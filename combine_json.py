"""
Combine multiple JSON files into a single file
"""

import json
import os

def combine_json_files(input_folder, output_file):
    combined_data = []

    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                # Load the JSON data from each file
                data = json.load(file)
                combined_data.extend(data)

    # Write the combined data to the output file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(combined_data, output_file, indent=2)

# Example usage
input_folder = 'json_files'
output_file = 'goodreads_data.json'
combine_json_files(input_folder, output_file)