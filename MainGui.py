import tkinter as tk
from tkinter import ttk
import json  # Import the json module to work with JSON files

cluster_id = None

def update_json_with_user_input(cluster_id, user_input):
    try:
        with open(json_file_path, 'r+') as file:
            data = json.load(file)
            # Assuming you want to add the user input to a specific cluster's "UserInput"
            if cluster_id in data:
                data[cluster_id]["UserInput"] = user_input
            else:
                # If the cluster does not exist, create a new cluster with the user input
                print("Error writing to JSON: Cluster ID not found")
            # Move the cursor to the beginning of the file to overwrite it
            file.seek(0)
            # Write the modified data back to the file
            json.dump(data, file, indent=4)
            # Truncate the file to the new size
            file.truncate()
    except IOError as e:
        print("An error occurred while writing to the JSON file:", e)

def on_enter_click():
    cluster_id = "39"  # Example cluster ID, adjust as needed or get from user input
    user_text = user_input.get()
    print("User input to add to JSON:", user_text)
    update_json_with_user_input(cluster_id, user_text)
    # Optional: Clear the input field after adding the input to JSON
    user_input.delete(0, tk.END)



def load_data_from_json(json_file_path):
    with (open(sentences_file_path, "r")) as sentencesFile:
        sentences = sentencesFile.readlines()

    with (open(labels_file_path, "r")) as labelsFile:
        # labels = labelsFile.readlines()
        label_lines = [line.strip().split() for line in labelsFile]

    with open(json_file_path, "r") as jsonFile:
        data = json.load(jsonFile)
        clusterNum = next(iter(data))
        cluster_id = clusterNum
        Entries = data[clusterNum]["Entries"]
        for entry in Entries:
            token = entry["Word"]
            sentence = sentences[int(entry["SentID"])]
            print(entry["SentID"], ":", entry["TokenID"])
            token_label = label_lines[int(entry["SentID"])][int(entry["TokenID"])]
            treeview.insert("", tk.END, values=(token,token_label, sentence))

        LLMlabels = data[clusterNum]["Labels"]
        labels_text.configure(state="normal")  
        labels_text.delete("1.0", tk.END)  
        for label in LLMlabels[:3]:  
            labels_text.insert(tk.END, label + "\n\n")  
        labels_text.configure(state="disabled") 


root = tk.Tk()
root.title("Labelling Tool")

# Create a top frame for user input
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X)

# Label for the input
input_label = tk.Label(top_frame, text="How would you label this cluster:")
input_label.pack(side=tk.LEFT, padx=(10, 2), pady=10)

# Entry widget for the input
user_input = tk.Entry(top_frame)
user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10), pady=10)

# Enter button next to the input
enter_button = tk.Button(top_frame, text="Enter", command=lambda: print("Entered text:", user_input.get()))
enter_button.pack(side=tk.LEFT, padx=(10, 0), pady=10)

# Frame for displaying labels, placed below the user input and above the Treeview
labels_frame = tk.Frame(root, height=100)  # Adjust height as needed
labels_frame.pack(fill=tk.X, pady=10)

# Title label for the LLM Suggestions Text widget
llm_title_label = tk.Label(labels_frame, text="LLM Suggestions", font=("Arial", 12, "bold"))
llm_title_label.pack(side=tk.TOP, fill=tk.X)

# Text widget for displaying labels
labels_text = tk.Text(labels_frame, height=4, wrap="word")
labels_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
labels_text.configure(state="disabled")  # Start as read-only

# Scrollbar for the Text widget
labels_scroll = ttk.Scrollbar(labels_frame, orient="vertical", command=labels_text.yview)
labels_scroll.pack(side=tk.RIGHT, fill="y")
labels_text.configure(yscrollcommand=labels_scroll.set)

# Create a frame for the Treeview widget to allow for more flexible resizing
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Define the Treeview widget with the desired columns
treeview = ttk.Treeview(frame, columns=("Cluster # words", "Token Label", "Sentence Context"), show="headings")
treeview.heading("Cluster # words", text="Words from Cluster #")
treeview.heading("Token Label", text="Token's Label")
treeview.heading("Sentence Context", text="Context from Sentence")
treeview.column("Cluster # words", stretch=tk.YES)
treeview.column("Token Label", stretch=tk.YES)
treeview.column("Sentence Context", stretch=tk.YES)
treeview.pack(fill=tk.BOTH, expand=True)


enter_button.config(command=on_enter_click)

# Load JSON data and display labels
json_file_path = "enriched_cluster_labels.json"
sentences_file_path = "codetest2_test_unique.in"
labels_file_path = "codetest2_test_unique.label"
load_data_from_json(json_file_path)

root.mainloop()


