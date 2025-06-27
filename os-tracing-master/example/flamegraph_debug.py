import json

# Load and read the JSON file
with open('output-directjson.json', 'r') as file:
    data = json.load(file)

    # Ask user for input
    keep_count = int(input("How many trace events (total: "+ str(len(data['traceEvents'])) +")would you like to keep? "))

    # Trim the trace events array
    data['traceEvents'] = data['traceEvents'][:keep_count]

    # Write back to output-directjson-slice.json
    with open('output-directjson-slice.json', 'w') as output_file:
        json.dump(data, output_file, indent=4)
    print(f"Trimmed JSON data has been written to output-directjson-slice.json")