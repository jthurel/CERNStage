import tkinter as tk
from tkinter import filedialog

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

        # Afficher les lignes lues sans commentaires
        for ligne in lignes_sans_commentaires:
            print(ligne)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Sélection de fichier")

# Création d'un bouton pour sélectionner un fichier
select_button = tk.Button(root, text="Sélectionner un fichier", command=select_file)
select_button.pack(pady=20)

# Création d'une étiquette pour afficher le chemin du fichier sélectionné
label = tk.Label(root, text="")
label.pack()

# Lancement de la boucle principale
root.mainloop()