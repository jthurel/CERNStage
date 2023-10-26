import tkinter as tk
from tkinter import filedialog
import os
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=1)

#global variables
fileofinterest = []

# Fonction pour gérer l'action du bouton "Search Port"
#def search_port():
    # Ici, vous pouvez effectuer une action pour rechercher un port#
    #search_result.set("Résultat de la recherche du port")
def search_port():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=19200, timeout=2)
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            ser.close()

            if "GP102" in response:
                search_result.set(port.device)
                return port.device # return the found port if existing
        except (OSError, serial.SerialException):
            continue

    search_result.set("Aucun port trouvé")  # Met à jour le champ de texte en cas d'absence de port
    return None

file_name= ''
# Fonction pour gérer l'action du bouton "Upload Config"
# Fonction pour gérer l'action du bouton "Upload Config"
def upload_config():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        fileofinterest.clear()  # Clear the list
        fileofinterest.append(file_name)  # Append the file name to the list
        fileofinterest.append(file_path)  # Append the file path to the list
        upload_entry.delete(0, tk.END)  # Clear the current text in the entry
        upload_entry.insert(0, file_name)  # Display the file name in the entry field

########################################################################"
# Fonction pour gérer l'action du bouton "Send config file"
#def send_config():
    # Ici, vous pouvez effectuer une action pour rechercher un port
#    send_config_result.set("Status de l'envoi du fichier")
#########################################################################
#file_path = filedialog.askopenfilename()
#if file_path:
#    file_name = os.path.basename(file_path)
def lire_fichier_sans_commentaires(file_path):
    lignes_lues = []

    try:
        with open(file_path, 'r') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()  # Supprimer les espaces et les sauts de ligne au début et à la fin
                if not ligne.startswith("#"):
                    lignes_lues.append(ligne)

    except FileNotFoundError:
        print(f"Le fichier '{filepath}' est introuvable.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")

    return lignes_lues

#def select_file():
 #   file_path = filedialog.askopenfilename()
  #  if file_path:
   #     label.config(text=f"Fichier sélectionné : {file_path}")
    #    send(file_path)

#def send_config(fileofinterest):
def send_config():
    #global file_path
    #file_path = filedialog.askopenfilename()
    ##selected_file_path = fileofinterest[1]
    global fileofinterest  # Declare fileofinterest as a global variable
    if fileofinterest:
        selected_file_path = fileofinterest[1]
    #if file_path:
        lignes_sans_commentaires = lire_fichier_sans_commentaires(selected_file_path)
        for line in lignes_sans_commentaires:
            # Divisez chaque ligne en deux parties (nom de commande et valeur)
            parts = line.strip().split(',')
            if len(parts) == 2:
                command, value = parts
                # Envoyez la commande et la valeur via le port série
                ser.write(f"{command},{value}\n".encode())

    #lignes_sans_commentaires = lire_fichier_sans_commentaires(file_path)

    #for line in lignes_sans_commentaires:
        # Divisez chaque ligne en deux parties (nom de commande et valeur)
     #   parts = line.strip().split(',')
     #   if len(parts) == 2:
     #       command, value = parts
     #       # Envoyez la commande et la valeur via le port série
     #       ser.write(f"{command},{value}\n".encode())

####################################################################################
# Fonction pour gérer l'action du bouton "View config file"
def view_config():
    # Ici, vous pouvez effectuer une action pour rechercher un port
    view_config_result.set("Status de l'envoi du fichier")
######################################################################################
# Fonction pour gérer l'action du bouton "View sinus signal"
#def view_signal():
    # Ici, vous pouvez effectuer une action pour rechercher un port
#    view_signal_result.set("Status de l'envoi du fichier")

def find(fichier, mot, position):
    try:
        with open(fichier, 'r') as file:
            for line in file:
                if mot in line:
                    parts = line.split(',')
                    if len(parts) > position:
                        value = parts[position].strip()
                        if value.isnumeric():
                            return int(value)
                        elif value.replace('.', '', 1).isdigit():
                            return float(value)
        return None  # Si le mot n'est pas trouvé ou la position est invalide
    except FileNotFoundError:
        print(f"Le fichier '{fichier}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

#Type= find(file_name,

def view_signal(Type, amplit, offset, freqStart, freqEnd):
    # Période d'échantillonnage
    Period_start = 1.0 / freqStart # periode du signal de départ (le temps d'avoir une sinus complete)
    Period_end= 1.0 / freqEnd      # periode du signal de fin (le temps d'avoir une sinus complete) T_end << T_start

    # Créer un tableau de temps pour une période de chaque sinus
    table_start = 1*np.linspace(0, Period_start, 1000) # disposer d'un nombre de points suffisamment important pour tracer la sinus (1000 point par défaut)
    table_end = 5*np.linspace(0, Period_end, 1000)

    if Type == "sinus":
        # Créer les signaux sinusoidaux
        signal_start = amplit * np.sin(2 * np.pi * freqStart * table_start) + offset
        signal_end = amplit * np.sin(2 * np.pi * freqEnd * table_end) + offset

        # Créer la fenêtre du graphique
        fig, ax = plt.subplots(figsize=(10, 6))

        # Tracer le premier signal à gauche (en bleu par exemple)
        ax.plot(table_start, signal_start, color='darkblue')

        # Tracer le deuxième signal à droite (en bleu pour avoir la même couleur)
        ax.plot(table_end + 2*Period_start, signal_end, color='darkblue') # table_end + 2*Period_start > chaque point de table_end est décalé de 2xPeriod_start

        # Ajouter des étiquettes d'axe
        ax.set_xlabel("Temps")
        ax.set_ylabel("Amplitude")

        # Ajouter les valeurs d'amplitude, de fréquence de début et de fréquence de fin en dessous du graphique
        plt.text(-0.61*Period_start / 2, offset + (amplit / 2 ), f"Amplitude: {amplit}", fontsize=12, color='darkblue', horizontalalignment='center')
        plt.text(Period_start/2.5, -amplit+0.2, f"Fréq. de début: {freqStart} Hz", fontsize=12, color='darkblue', horizontalalignment='center')
        plt.text(2.0* Period_start, -amplit+0.2, f"Fréq. de fin: {freqEnd} Hz", fontsize=12, color='darkblue', horizontalalignment='center')

        # Afficher le graphique
        plt.show()
    else:
        print("Type de signal non pris en charge. Utilisez 'sinus'.")





##############################################################################################
# Fonction pour gérer l'action du bouton "Start sweep"
def Start_Sweep():
    # Ici, vous pouvez effectuer une action pour rechercher un port
    start_sweep_result.set("Status de l'envoi du fichier")

# Fonction pour gérer l'action du bouton "Abort sweep"
def Abort_Sweep():
    # Ici, vous pouvez effectuer une action pour rechercher un port
    abort_sweep_result.set("Status de l'envoi du fichier")

###############################################################################
# Fonction pour tout quitter
def button_quit():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to exit?\n\nAll processes will be stopped/killed.")
    if result == "yes":
        root.quit()
        root.destroy()
###############################################################################

# Créer la fenêtre principale
root = tk.Tk()
root.title("GP102 control board")

###############################################################################
# Créer le bouton "Search Port"
search_button = tk.Button(root, text="Search Port", command=search_port)
search_button.grid(row=0, column=0,columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Search Port"
search_result = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_result)
search_entry.grid(row=0, column=2, sticky="ew")
###############################################################################

###############################################################################
# Créer le bouton "Upload Config"
upload_button = tk.Button(root, text="Upload Config", command=upload_config)
upload_button.grid(row=1, column=0,columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
#upload_result = tk.StringVar()
#upload_entry = tk.Entry(root, textvariable=f"{fileofinterest[1]}")
#upload_entry.grid(row=1, column=2, sticky="ew")
upload_result = tk.StringVar()
upload_entry = tk.Entry(root)
upload_entry.grid(row=1, column=2, sticky="ew")
###############################################################################

###############################################################################
# Créer le bouton "Send Config"
send_config_button = tk.Button(root, text="Send Config to TFA", command=send_config)
send_config_button.grid(row=2, column=0, sticky="ew")

# Créer le bouton "View Config"
view_config_button = tk.Button(root, text="View Config file", command=view_config)
view_config_button.grid(row=2, column=1, sticky="ew")

# Créer le bouton "View signal(sinus)"
view_signal_button = tk.Button(root, text="View sinusoidal signal", command=view_signal)
view_signal_button.grid(row=2, column=2, sticky="ew")
###############################################################################

###############################################################################
# Créer le bouton "Start Sweep"
start_sweep_button = tk.Button(root, text="Start Sweep", command=Start_Sweep)
start_sweep_button.grid(row=4, column=0,columnspan=1, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
start_sweep_result = tk.StringVar()
start_sweep_entry = tk.Entry(root, textvariable=start_sweep_result)
start_sweep_entry.grid(row=4, column=2, sticky="ew")
###############################################################################

# Créer le bouton "Abort Sweep"
abort_sweep_button = tk.Button(root, text="Abort Sweep", command=Abort_Sweep)
abort_sweep_button.grid(row=4, column=1,columnspan=1, sticky="ew")
###############################################################################
# Créer les boutons pour "generator control"

label = tk.Label(root, text="Generator control :")
label.grid(row=3, column=0) # je créé du texte
generator_on_button = tk.Button(root, text="ON", command=search_port)
generator_on_button.grid(row=3, column=1,columnspan=1, sticky="ew")
generator_off_button = tk.Button(root, text="OFF", command=search_port)
generator_off_button.grid(row=3, column=2,columnspan=1, sticky="ew")
################################################################################
# Créer le bouton "select data folder"
data_folder_button = tk.Button(root, text="Select data folder", command=upload_config)
data_folder_button.grid(row=5, column=0,columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
data_folder_result = tk.StringVar()
data_folder_entry = tk.Entry(root, textvariable=upload_result)
data_folder_entry.grid(row=5, column=2, sticky="ew")
###############################################################################
# Créer le bouton "download data"
download_data_button = tk.Button(root, text="Download data", command=upload_config)
download_data_button.grid(row=6, column=0,columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
download_data_result = tk.StringVar()
download_data_entry = tk.Entry(root, textvariable=upload_result)
download_data_entry.grid(row=6, column=2, sticky="ew")
###############################################################################
bouton_quit = tk.Button(root, text="Quit", command=button_quit, bg="#FF0000")
bouton_quit.grid(row=7, column=2)