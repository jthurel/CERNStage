import tkinter as tk
from tkinter import filedialog
import os

def upload_config():
    selected_file = []  # Initialize selected_file as an empty list
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        selected_file.append(file_name)  # Append the file name to the list
        selected_file.append(file_path)  # Append the file path to the list
    return selected_file

root = tk.Tk()

# Créer le bouton "Upload Config"
fileofinterest = []  # Initialize fileofinterest as an empty list
upload_button = tk.Button(root, text="Upload Config", command=lambda: fileofinterest.extend(upload_config()))
upload_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
upload_result = tk.StringVar()
upload_entry = tk.Entry(root, textvariable=f"{fileofinterest[0]}")
upload_entry.grid(row=1, column=2, sticky="ew")

root.mainloop()