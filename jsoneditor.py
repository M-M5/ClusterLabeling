import json

# Path to your JSON file
json_file_path = 'Arushis_Super_Cool_Clusters.json'

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
delete_first_50_json_objects(json_file_path)
delete_first_50_json_objects(json_file_path)
delete_first_50_json_objects(json_file_path)
retain_up_to_50_json_objects(json_file_path)


with open(json_file_path, 'r') as file:
    data = json.load(file)

print(len(data.keys()))

