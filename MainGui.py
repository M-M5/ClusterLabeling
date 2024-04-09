import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import json  # Import the json module to work with JSON files

import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# from nltk.corpus import stopwords

cluster_id = None
cluster_id = None
current_cluster_index = 0
clusters_data = None


def update_json_with_user_input(cluster_id, user_input):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if cluster_id in data:
            data[cluster_id]["UserInput"] = user_input
        else:
            print(f"Error writing to JSON: Cluster ID {cluster_id} not found")

        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print("An error occurred while writing to the JSON file:", e)

def load_next_cluster_data():
    global current_cluster_index, clusters_data
    cluster_ids = list(clusters_data.keys())
    print("load_next_cluster_data() called, current_cluster_index:", current_cluster_index, "Cluster IDs:", cluster_ids)
    if current_cluster_index < len(cluster_ids):
        current_cluster = cluster_ids[current_cluster_index]
        load_cluster_data(current_cluster)
    else:
        print("No more clusters to display.")

def load_cluster_data(cluster_id):
    global current_cluster_index, clusters_data

    with (open(sentences_file_path, "r")) as sentencesFile:
        sentences = sentencesFile.readlines()

    with (open(labels_file_path, "r")) as labelsFile:
        label_lines = [line.strip().split() for line in labelsFile]

    # Clear the Treeview and Labels Text widget
    treeview.delete(*treeview.get_children())
    labels_text.configure(state="normal")
    labels_text.delete("1.0", tk.END)

    cluster_data = clusters_data[cluster_id]
    Entries = cluster_data["Entries"]

    for entry in Entries:
        token = entry["Word"]
        sentence_id = int(entry["SentID"])
        token_id = int(entry["TokenID"])
        word_id = int(entry["WordID"])
        print("WordID", word_id, ",Token:", token, ",Sentence ID:", sentence_id, ",Token ID:", token_id)
        try:
            sentence = sentences[sentence_id]
            token_label = label_lines[sentence_id][token_id]
            treeview.insert("", tk.END, values=(word_id, token, token_label, sentence))
        except:
            print(f"Skipping entry: SentID {sentence_id}, TokenID {token_id} is out of range.")

    LLMlabels = cluster_data["Labels"]
    for label in LLMlabels[:3]:
        labels_text.insert(tk.END, label + "\n\n")
    labels_text.configure(state="disabled")

def on_enter_click():
    global current_cluster_index
    current_cluster = list(clusters_data.keys())[current_cluster_index]
    user_text = user_input.get()
    print("User input to add to JSON:", user_text)
    update_json_with_user_input(current_cluster, user_text)
    user_input.delete(0, tk.END)
    current_cluster_index += 1
    load_next_cluster_data()


def load_data_from_json(json_file_path):
    global clusters_data
    with (open(sentences_file_path, "r")) as sentencesFile:
        sentences = sentencesFile.readlines()

    with (open(labels_file_path, "r")) as labelsFile:
        label_lines = [line.strip().split() for line in labelsFile]

    with open(json_file_path, "r") as jsonFile:
        clusters_data = json.load(jsonFile)

    load_next_cluster_data()

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
treeview = ttk.Treeview(frame, columns=("WordID", "Cluster # words", "Token Label", "Sentence Context"), show="headings")
treeview.heading("WordID", text="Word ID")
treeview.heading("Cluster # words", text="Words from Cluster #")
treeview.heading("Token Label", text="Token's Label")
treeview.heading("Sentence Context", text="Context from Sentence")
treeview.column("Cluster # words", stretch=tk.YES)
treeview.column("Token Label", stretch=tk.YES)
treeview.column("Sentence Context", stretch=tk.YES)
treeview.pack(fill=tk.BOTH, expand=True)

customFont = tkFont.Font(family="Helvetica", size=12)  # Adjust the size as needed
style = ttk.Style()
style.configure("Treeview", font=customFont, rowheight=customFont.metrics("linespace"))


enter_button.config(command=on_enter_click)


json_file_path = "enriched_cluster_labels.json"
sentences_file_path = "codetest2_test_unique.in"
labels_file_path = "codetest2_test_unique.label"

with open(json_file_path, "r") as jsonFile:
    clusters_data = json.load(jsonFile)

load_next_cluster_data();


root.mainloop()


