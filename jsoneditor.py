import json

# Path to your JSON file
json_file_path = '451-500.json'

def delete_first_50_json_objects(json_file_path):
    try:
        # Open and load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Assuming the JSON structure is a dictionary where each key maps to a list
        keys_to_delete = list(data.keys())[:50]  # Get the first 50 keys

        for key in keys_to_delete:
            del data[key]  # Delete the key from the dictionary

        # Write the updated data back to the file
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print("First 50 JSON objects have been deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def retain_up_to_50_json_objects(json_file_path):
    try:
        # Open and load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Assuming the JSON structure is a dictionary where each key maps to a list
        keys = list(data.keys())  # Get all keys
        if len(keys) > 50:
            keys_to_retain = keys[:50]  # Identify the first 50 keys to retain
            # Create a new dictionary with only the first 50 objects
            data = {key: data[key] for key in keys_to_retain}

            # Write the updated data back to the file
            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print("JSON file has been updated to retain only up to the first 50 objects.")
        else:
            print("JSON file contains 50 or fewer objects. No changes made.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function with your JSON file path
# delete_first_50_json_objects(json_file_path)
# delete_first_50_json_objects(json_file_path)
# delete_first_50_json_objects(json_file_path)
# delete_first_50_json_objects(json_file_path)
# delete_first_50_json_objects(json_file_path)
# delete_first_50_json_objects(json_file_path)
# delete_first_50_json_objects(json_file_path)
# delete_first_50_json_objects(json_file_path)
# delete_first_50_json_objects(json_file_path)
# retain_up_to_50_json_objects(json_file_path)

# files=['1-50.json','51-100.json', '101-150.json', '151-200.json', '201-250.json', '251-300.json', '301-350.json', '351-400.json', '401-450.json', '451-500.json']

# with open('merged_clusters.json', "w") as outfile:
#    outfile.write('{}'.format('\n'.join([open(f, "r").read() for f in files])))

# with open(json_file_path, 'r') as file:
#     data = json.load(file)



json_file_path = "merged_clusters.json"
labels_file_path = "codetest2_test_unique.label"

with open(json_file_path, "r") as jsonFile:
    clusters_data = json.load(jsonFile)

# load_next_cluster_data();
cluster_ids = list(clusters_data.keys())
print(len(cluster_ids))

# print(len(data.keys()))