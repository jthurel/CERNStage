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
        selected_file.append(os.path.dirname(file_path))
        selected_file.append(os.path.getsize(file_path))
    return selected_file

# Mettez à jour le champ de texte lorsqu'un fichier est sélectionné
def update_entry(variable, upload_data):
    if variable:
        upload_data.set(variable[0])
    else:
        upload_data.set("")  # Effacez le champ de texte s'il n'y a pas de fichier sélectionné

root = tk.Tk()

################################################################################################################
# Créer le bouton "Upload source"
source = []  # Initialize as an empty list
upload_button = tk.Button(root, text="Upload Config", command=lambda: [source.extend(upload_config()), update_entry(source, text_source)]) # append could be used as well
upload_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
text_source = tk.StringVar() # obliged to create a string variable compatible with tinker
upload_entry = tk.Entry(root, textvariable=text_source)
upload_entry.grid(row=1, column=2, sticky="ew")
################################################################################################################

################################################################################################################
# Créer le bouton "Upload source"
destination = []  # Initialize as an empty list
upload_button = tk.Button(root, text="Upload Config", command=lambda: [destination.extend(upload_config()), update_entry(destination, text_destination)]) # append could be used as well
upload_button.grid(row=2, column=0, columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
text_destination = tk.StringVar() # obliged to create a string variable compatible with tinker
upload_entry = tk.Entry(root, textvariable=text_destination)
upload_entry.grid(row=2, column=2, sticky="ew")
################################################################################################################


root.mainloop()