import os
import tkinter as tk
from tkinter import filedialog

def create_and_open_config_file():
    # Spécifiez les valeurs du fichier de configuration
    config_data = """AMPLIT,3.0
    FREQUE,500
    OFFSET,1
    WAVEFO,SINEWA
    MODE,GAINPH
    FSWEEP,50,10,1000"""

    # Créez une fenêtre tkinter (invisible)


    # Demandez à l'utilisateur de choisir le dossier où enregistrer le fichier
    folder_path = filedialog.askdirectory()

    if folder_path:
        # Construisez le chemin complet du fichier en ajoutant le nom du fichier
        file_path = os.path.join(folder_path, 'config.txt')

        # Créez le fichier de configuration
        with open(file_path, 'w') as file:
            file.write(config_data)

        # Ouvrez le fichier avec un éditeur de texte
        os.system(f"xdg-open {file_path}")

# Utilisez la fonction pour créer et ouvrir le fichier de configuration
create_and_open_config_file()