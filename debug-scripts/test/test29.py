import subprocess
import platform
import tkinter as tk
from tkinter import filedialog

def creer_et_modifier_fichier(filepath):
    syst_os = platform.system()
    contenu_initial = """AMPLIT,3.0
FREQUE,500
OFFSET,1
WAVEFO,SINEWA
MODE,GAINPH
FSWEEP,50,10,1000"""  # Le contenu souhaité

    if syst_os == "Linux":
        subprocess.run(["touch", filepath])  # Crée le fichier sous Linux
    elif syst_os == "Windows":
        with open(filepath, "w") as file:
            file.write(contenu_initial)  # Crée le fichier sous Windows
    else:
        print("Système d'exploitation non pris en charge.")
        return

    # Ouvrir le fichier avec l'éditeur de texte par défaut
    if syst_os == "Linux":
        subprocess.run(["xdg-open", filepath])
    elif syst_os == "Windows":
        subprocess.run(["start", filepath], shell=True)

    # Attendre que l'utilisateur ait terminé d'éditer le fichier
    input("Appuyez sur Entrée une fois que vous avez terminé de modifier le fichier...")

    # Lire le contenu modifié du fichier
    with open(filepath, "r") as file:
        contenu_modifie = file.read()

    print("Contenu du fichier modifié :")
    print(contenu_modifie)

# Demander à l'utilisateur de sélectionner l'emplacement et le nom du fichier
root = tk.Tk()
root.withdraw()  # Cache la fenêtre principale de tkinter
filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])

if not filepath:
    print("Aucun emplacement de fichier sélectionné.")
else:
    creer_et_modifier_fichier(filepath)


