import tkinter as tk
from tkinter import filedialog
import os
import time
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox


#global variables
fileofinterest = []

# Fonction pour gérer l'action du bouton "Search Port"
#def search_port():
    # Ici, vous pouvez effectuer une action pour rechercher un port#
    #search_result.set("Résultat de la recherche du port")

##############################################################
def search_port():
    #port.device=""
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=19200, timeout=2)
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            ser.close()

            if "GP102" in response:
                #search_result.set(port.device)
                return port.device # return the found port if existing
        except (OSError, serial.SerialException):
            continue

    #search_result.set("Aucun port trouvé")  # Met à jour le champ de texte en cas d'absence de port
    return "Aucun port trouvé"

#########################################################################################

# Mettez à jour le champ de texte lorsqu'un fichier est sélectionné
def update_search_result():
    port = search_port()
    search_result.set(port) #Effacez le champ de texte s'il n'y a pas de fichier sélectionné

######################################################################################

#port= search_port()
#print (port)
#ser = serial.Serial(port, baudrate=19200, timeout=1)

port = search_port()
if port != "Aucun port trouvé":
    ser = serial.Serial(port, baudrate=19200, timeout=1)
    # Continuer avec le port série
else:
    print("Problème : aucun port trouvé")


###############################################################


# Fonction pour gérer l'action du bouton "Upload Config"
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

###############################################################################

###############################################################################

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

####################################################################


####################################################################
def send_config(file, port):
    status = "The data has been received by the device"
    if file:
        selected_file_path = file[1]
        lignes_sans_commentaires = lire_fichier_sans_commentaires(selected_file_path)
        for line in lignes_sans_commentaires:
            # Divisez chaque ligne en parties (nom de commande, valeur1, valeur2, valeur3)
            parts = line.strip().split(',')
            if 1 <= len(parts) <= 4:  # Vous pouvez avoir de 1 à 4 éléments
                command = parts[0]
                values = parts[1:]  # Les valeurs peuvent être vides si elles sont absentes
                # Envoyez la commande et les valeurs via le port série
                port.write(f"{command},{','.join(values)}\n".encode())
                port.write(bytes("*ESR?", 'utf-8') + b'\r')
                response = port.readline().decode('ascii')
                if response.strip() != '0':  # Si la réponse n'est pas 0, cela signifie qu'il y a un problème dans le fichier de configuration
                    print("Problème dans votre fichier de configuration : ", command, response)
                    status = "Veuillez corriger votre fichier de configuration"
    return status
###########################################################################

def send_command(command,serial_obj):
    if serial_obj != "Aucun port trouvé":

        if command == "ON":
            serial_obj.write(bytes("OUTPUT,ON", 'utf-8') + b'\r')
        elif command == "OFF":
            serial_obj.write(bytes("OUTPUT,OFF", 'utf-8') + b'\r')
    else:
        print("Aucun port serie n'est défini.")

############################################################################

# Fonction appelée lorsque le bouton "ON" est cliqué
def turn_on():
    if 'ser' in globals():
        send_command("ON", ser)
    else:
        print("Aucun port série n'est défini.")

# Fonction appelée lorsque le bouton "OFF" est cliqué
def turn_off():
    if 'ser' in globals():
        send_command("OFF", ser)
    else:
        print("Aucun port série n'est défini.")
####################################################################################
# Fonction pour gérer l'action du bouton "View config file"
def view_config(config_file):
    if config_file:
        try:
            with open(config_file, 'r') as file:
                content = file.read()
                # Créer une nouvelle fenêtre pour afficher le contenu
                view_window = tk.Toplevel(root)
                view_window.title("Contenu du fichier de configuration")
                text_widget = tk.Text(view_window)
                text_widget.insert(tk.END, content)
                text_widget.pack()
            return "Contenu du fichier de configuration affiché"
        except Exception as e:
            return f"Erreur lors de l'affichage du fichier de configuration : {e}"
    return "Aucun fichier de configuration sélectionné"

    #view_config_result.set("Status de l'envoi du fichier")
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



###############################################################################################

##############################################################################################
# Fonction pour gérer l'action du bouton "Start sweep"
def Start_Sweep():
    with serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=2) as ser:
        ser.write(bytes("START", 'utf-8') + b'\r')
    #start_sweep_result.set("Status de l'envoi du fichier")

###############################################################################################

#####################################################################################

# Fonction pour gérer l'action du bouton "Abort sweep"
def Abort_Sweep():
    with serial.Serial('port', baudrate=19200, timeout=2) as ser:
        ser.write(bytes("ABORT", 'utf-8') + b'\r')
    #abort_sweep_result.set("Status de l'envoi du fichier")

###############################################################################################

###############################################################################

# Fonction pour gérer l'action du bouton "select data folder"
def select_folder():
    selected_folder = []  # Initialize selected_file as an empty list
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_name = os.path.basename(folder_path)
        selected_folder.append(folder_path)  # Append the file path to the list
        #selected_folder.append(os.path.dirname(folder_path))
    return selected_folder

def update_folder_entry(variable, upload_data):
    if variable:
        upload_data.set(variable[0])
    else:
        upload_data.set("")  # Effacez le champ de texte s'il n'y a pas de fichier sélectionné
################################################################################

###############################################################################################

# Fonction pour gérer l'action du bouton "download data"
def upload_config():
    #global state
    results = ""
    ser.reset_input_buffer()
    ser.write(bytes("DAV?", 'UTF-8') + b'\r')
    time.sleep(0.5)
    while ser.in_waiting < 0:
        pass
    while ser.in_waiting > 0:
        data_ready = ser.read(ser.in_waiting).decode('ascii')
    if "15" in data_ready:
        ser.reset_input_buffer()
        ser.write(bytes("GAINPH?SWEEP", 'UTF-8') + b'\r')
        while ser.in_waiting <= 0:
            pass
        while ser.in_waiting > 0:
            results += ser.read(ser.in_waiting).decode('ascii')
            time.sleep(0.05)
        results = "Frequency,Magnitude_1,Magnitude_2,dB,Phase\n" + results
        print(results)
        with open('test.csv', "w", encoding="utf-8") as f:
            f.write(results.replace("\r", ""))
    #upload_result_result.set("Status de l'envoi du fichier")

#####################################################################################

###############################################################################################

# Fonction pour tout quitter
def button_quit():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to exit?\n\nAll processes will be stopped/killed.")
    if result == "yes":
        root.quit()
        root.destroy()
#########################################################################################################################################################################
#########################################################################################################################################################################
# Créer la fenêtre principale
root = tk.Tk()
root.title("GP102 control board")

###############################################################################

###############################################################################

search_result = tk.StringVar()
search_port_button = tk.Button(root, text="Search Port", command=update_search_result)
search_port_button.grid(row=0, column=0, columnspan=2, sticky="ew")

# Create the text field to display the found port
search_port_entry = tk.Entry(root, textvariable=search_result)
search_port_entry.grid(row=0, column=2, sticky="ew")
###############################################################################

###############################################################################
# Créer le bouton "Upload source / config file"
source = []  # Initialize as an empty list
upload_button = tk.Button(root, text="Upload Config", command=lambda: [source.append(upload_config()), update_entry(source, text_source)]) # append could be used as well
upload_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
text_source = tk.StringVar() # obliged to create a string variable compatible with tinker
upload_entry = tk.Entry(root, textvariable=text_source)
upload_entry.grid(row=1, column=2, sticky="ew")


###############################################################################

###############################################################################

# Créer le bouton "Send Config"
send_config_button = tk.Button(root, text="Send Config to TFA", command=send_config(fileofinterest,port))
send_config_button.grid(row=2, column=0, sticky="ew")

###############################################################################

###############################################################################

# Créer le bouton "View Config"
view_config_button = tk.Button(root, text="View Config file", command=view_config)
view_config_button.grid(row=2, column=1, sticky="ew")

###############################################################################

###############################################################################

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

###############################################################################

# Créer le bouton "Abort Sweep"
abort_sweep_button = tk.Button(root, text="Abort Sweep", command=Abort_Sweep)
abort_sweep_button.grid(row=4, column=1,columnspan=1, sticky="ew")
###############################################################################
# Créer les boutons pour "generator control"

label = tk.Label(root, text="Generator control :")
label.grid(row=3, column=0) # je créé du texte
generator_on_button = tk.Button(root, text="ON", command=turn_on)
generator_on_button.grid(row=3, column=1,columnspan=1, sticky="ew")
generator_off_button = tk.Button(root, text="OFF", command=turn_off)
generator_off_button.grid(row=3, column=2,columnspan=1, sticky="ew")
################################################################################
# Créer le bouton "select data folder"
Folder=[]
data_folder_button = tk.Button(root, text="Select data folder", command=lambda: [Folder.extend(select_folder()), update_folder_entry(Folder, data_folder_result)])
data_folder_button.grid(row=5, column=0,columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Select data folder"
data_folder_result = tk.StringVar()
data_folder_entry = tk.Entry(root, textvariable=data_folder_result)
data_folder_entry.grid(row=5, column=2, sticky="ew")
###############################################################################
# Créer le bouton "download data"
download_data_button = tk.Button(root, text="Download data", command=upload_config)
download_data_button.grid(row=6, column=0,columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
download_data_result = tk.StringVar()
download_data_entry = tk.Entry(root, textvariable=data_folder_result)
download_data_entry.grid(row=6, column=2, sticky="ew")
###############################################################################
bouton_quit = tk.Button(root, text="Quit", command=button_quit, bg="#FF0000")
bouton_quit.grid(row=7, column=2)