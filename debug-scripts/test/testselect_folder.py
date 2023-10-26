import tkinter as tk
from tkinter import filedialog

def select_folder():
    # Afficher la boîte de dialogue de sélection de dossier
    folder_path = filedialog.askdirectory()

    # Vérifier si un dossier a été sélectionné
    if folder_path:
        print("Dossier sélectionné :", folder_path)
        # Vous pouvez utiliser 'folder_path' pour enregistrer votre fichier dans le dossier sélectionné
    else:
        print("Aucun dossier sélectionné.")

# Créer une fenêtre tkinter pour tester la fonction
root = tk.Tk()
root.title("Sélection de dossier")

# Créer un bouton pour déclencher la fonction
select_folder_button = tk.Button(root, text="Sélectionner un dossier", command=select_folder)
select_folder_button.pack()

root.mainloop()