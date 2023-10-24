import tkinter as tk
from tkinter import filedialog
import serial
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1) #/Dev/ttyUSB0 has to be a variable determined by the function "which serial port"

#Read file without comment, remains only: command_name,command_value1,command_value2,...

def lire_fichier_sans_commentaires(filepath):
    lignes_lues = []

    try:
        with open(filepath, 'r') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()  # Supprimer les espaces et les sauts de ligne au début et à la fin
                if not ligne.startswith("#"):
                    lignes_lues.append(ligne)

    except FileNotFoundError:
        print(f"Le fichier '{filepath}' est introuvable.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")

    return lignes_lues

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text=f"Fichier sélectionné : {file_path}")
        lignes_sans_commentaires = lire_fichier_sans_commentaires(file_path)

        for line in lignes_sans_commentaires:
            # Divisez chaque ligne en parties (nom de commande, valeur1, valeur2, valeur3)
            parts = line.strip().split(',')
            if 1 <= len(parts) <= 4:  # Vous pouvez avoir de 1 à 4 éléments
                command = parts[0]
                values = parts[1:]  # Les valeurs peuvent être vides si elles sont absentes
                # Envoyez la commande et les valeurs via le port série
                ser.write(f"{command},{','.join(values)}\n".encode())

# Création de la fenêtre principale
root = tk.Tk()
root.title("Sélection de fichier")

# Création d'un bouton pour sélectionner un fichier
select_button = tk.Button(root, text="Sélectionner un fichier", command=select_file)
select_button.pack(pady=20)

# Création d'une étiquette pour afficher le chemin du fichier sélectionné
label = tk.Label(root, text="")
label.pack()

# Lancer la boucle principale de tkinter
root.mainloop()