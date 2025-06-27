import json

# Load and read the JSON file
with open('output-directjson.json', 'r') as file:
    data = json.load(file)

    # Ask user index range to show
    start_index = int(input("Enter the start index of trace events to keep (total: "+ str(len(data['traceEvents'])) +"): "))
    end_index = int(input("Enter the end index of trace events to keep (total: "+ str(len(data['traceEvents'])) +"): "))

    # Print the selected range of trace events
    for i in range(start_index, end_index+1):
        print(f"Trace Event {i}: {data['traceEvents'][i]}")