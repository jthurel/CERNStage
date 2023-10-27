import tkinter as tk
from tkinter import filedialog
import os
import time
import serial
import datetime
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
import subprocess
import platform

#global variables
global file
global dir_folder


##############################################################
# Fonction pour gérer l'action du bouton "Search Port"
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

###############################################################

# Fonction pour gérer l'action du bouton "Upload Config"
def upload_config():
    source.clear()
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
        upload_data.set(variable[0][0])
        send_config_button.config(state="active")
        view_config_button.config(state="active")
        view_signal_button.config(state="active")
        generator_on_button.config(state="active")
        generator_off_button.config(state="active")
    else:
        upload_data.set("")  # Effacez le champ de texte s'il n'y a pas de fichier sélectionné
        send_config_button.config(state="disabled")
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
def send_config(fileofinterest, port):
    x=1
    error_name=[]
    status = "The data has been received by the device"
    #fileofinterest="/home/jthurel/Documents/CERNScripts/config file/compact_config"
    if fileofinterest:
        selected_file_path= fileofinterest[0][1]
        #print(fileofinterest)
        lignes_sans_commentaires = lire_fichier_sans_commentaires(selected_file_path)
        for line in lignes_sans_commentaires:
            # Divisez chaque ligne en parties (nom de commande, valeur1, valeur2, valeur3)
            parts = line.strip().split(',')
            if 1 <= len(parts) <= 4:  # Vous pouvez avoir de 1 à 4 éléments
                command = parts[0]
                values = parts[1:]  # Les valeurs peuvent être vides si elles sont absentes
                # Envoyez la commande et les valeurs via le port série
                ser = serial.Serial(port, baudrate=19200, timeout=1)
                ser.write(f"{command},{','.join(values)}\n".encode())
                ser.write(bytes("*ESR?", 'utf-8') + b'\r')
                response = ser.readline().decode('ascii')
                if response.strip() != '0':  # Si la réponse n'est pas 0, cela signifie qu'il y a un problème dans le fichier de configuration
                    error_name.append( command)
                    print("Problème dans votre fichier de configuration : ", command, response)
                    status = "Please correct your configuration file :" , error_name
                    x=0
    root.after(2000, activate_start_sweep_button(x)) #laisse le temps à l'appareil de recevoir les données
    send_config_result.set(status)
    print (status)
    return status

def activate_start_sweep_button(x):
    if x == 1:
        start_sweep_button.config(state="active")
        start_sweep_result.set("Ready to sweep")
    else:
        start_sweep_result.set("Can't sweep, config error")
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
    generator_on_button.config(bg="#00FF57")
    generator_off_button.config(bg="lightgrey")
    if 'ser' in globals():
        send_command("ON", ser)
    else:
        print("Aucun port série n'est défini.")

# Fonction appelée lorsque le bouton "OFF" est cliqué
def turn_off():
    generator_off_button.config(bg="red")
    generator_on_button.config(bg="lightgrey")
    if 'ser' in globals():
        send_command("OFF", ser)
    else:
        print("Aucun port série n'est défini.")
####################################################################################

#####################################################################################
# Fonction pour gérer l'action du bouton "View config file"
def view_config(fileofinterest):

    if fileofinterest:
        selected_file_path= fileofinterest[0][1]
        syst_os = platform.system()
        if syst_os == "Linux":
            subprocess.run(["xdg-open", selected_file_path])
        elif syst_os == "Windows":
            subprocess.run(["start", selected_file_path], shell=True)
        else:
            print("Système d'exploitation non pris en charge.")


######################################################################################

################################################################################
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

#########################################################################################

#########################################################################################

def view_signalinit(Type, amplit, offset, freqStart, freqEnd):
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
        plt.text(-0.6*Period_start / 2, offset + (amplit / 2 ), f"Amplitude: {amplit}", fontsize=12, color='darkblue', horizontalalignment='center')
        plt.text(Period_start/2.5, -amplit+0.2, f"Fréq. de début: {freqStart} Hz", fontsize=12, color='darkblue', horizontalalignment='center')
        plt.text(2.0* Period_start, -amplit+0.2, f"Fréq. de fin: {freqEnd} Hz", fontsize=12, color='darkblue', horizontalalignment='center')

        # Afficher le graphique
        plt.show()
    else:
        print("Type de signal non pris en charge. Utilisez 'sinus'.")


def view_signal(fileofinterest):
    if fileofinterest:
        selected_file_path= fileofinterest[0][1]
    #valeur à calculer
        #typeform=find(selected_file_path, 'WAVEFO', 0)
        typeform="sinus"
        amplitude=find(selected_file_path, 'AMPLIT', 1)
        offset=find(selected_file_path, 'OFFSET', 1)
        freqstart=find(selected_file_path, 'FSWEEP', 2)
        freqend=find(selected_file_path, 'FSWEEP', 3)
        if typeform is not None and amplitude is not None and offset is not None and freqstart is not None and freqend is not None:
            return view_signalinit(typeform, amplitude, offset, freqstart, freqend)
        else:
            print("Les valeurs nécessaires ne sont pas définies.")
    else:
        print ("Error : be sure that is a sinus, this button only shows a graph of a sinus.")
        return None

###############################################################################################

##############################################################################################
# Fonction pour gérer l'action du bouton "Start sweep"
def Start_Sweepinit(port):
    start_sweep_button.config(bg="#00FF57")
    abort_sweep_button.config(bg="lightgrey")
    start_sweep_result.set("Sweeping ...")
    def reset_status():
        start_sweep_result.set("Sweep finished")

    # Planifie la réinitialisation du champ après 20 secondes
    root.after(20000, reset_status)# 1seconde = 1000

    print("sweep")
    ser = serial.Serial(port, baudrate=19200, timeout=1)
    ser.write(bytes("START", 'utf-8') + b'\r')


def Start_Sweep(port):
    # Désactivez tous les autres boutons sauf "Abort Sweep" et "Quit"
    search_port_button.config(state="disabled")
    upload_button.config(state="disabled")
    send_config_button.config(state="disabled")
    view_config_button.config(state="disabled")
    view_signal_button.config(state="disabled")
    generator_on_button.config(state="disabled")
    generator_off_button.config(state="disabled")
    data_folder_button.config(state="active")
    download_data_button.config(state="disabled")
    # Désactivez également le bouton "Start Sweep" pour éviter de lancer plusieurs fois le balayage
    start_sweep_button.config(state="disabled")
    # Activez le bouton "Abort Sweep" pour permettre l'arrêt du balayage
    abort_sweep_button.config(state="active")
    abort_sweep_button.config(bg="#EF0023")
    start_sweep_result.set("Sweeping ...")
    #Problème si abort sweep on doit quand meme attendre pour que les boutons soient réactivés.
    def reset_status():
        start_sweep_result.set("Sweep finished")
        # Réactivez tous les autres boutons après la fin du balayage
        search_port_button.config(state="active")
        upload_button.config(state="active")
        send_config_button.config(state="active")
        view_config_button.config(state="active")
        view_signal_button.config(state="active")
        generator_on_button.config(state="active")
        generator_off_button.config(state="active")
        data_folder_button.config(state="active")
        download_data_button.config(state="active")
        # Réactivez également le bouton "Start Sweep"
        start_sweep_button.config(state="active")
        # Désactivez le bouton "Abort Sweep" car le balayage est terminé
        abort_sweep_button.config(state="disabled")

    # Planifie la réinitialisation du champ et la réactivation des boutons après la fin du balayage
    root.after(20000, reset_status)
    print("sweep")
    ser = serial.Serial(port, baudrate=19200, timeout=1)
    ser.write(bytes("START", 'utf-8') + b'\r')


###############################################################################################

#####################################################################################

# Fonction pour gérer l'action du bouton "Abort sweep"
def Abort_Sweep(port):
    abort_sweep_button.config(bg="red")
    start_sweep_button.config(bg="lightgrey")
    start_sweep_result.set("Sweeping stopped")

    start_sweep_result.set("Sweep finished")
    # Réactivez tous les autres boutons après la fin du balayage
    search_port_button.config(state="active")
    upload_button.config(state="active")
    send_config_button.config(state="active")
    view_config_button.config(state="active")
    view_signal_button.config(state="active")
    generator_on_button.config(state="active")
    generator_off_button.config(state="active")
    data_folder_button.config(state="active")
    download_data_button.config(state="active")
    # Réactivez également le bouton "Start Sweep"
    start_sweep_button.config(state="active")
    # Désactivez le bouton "Abort Sweep" car le balayage est terminé
    abort_sweep_button.config(state="disabled")

    print("no sweep")
    with serial.Serial(port, baudrate=19200, timeout=2) as ser:
        ser.write(bytes("ABORT", 'utf-8') + b'\r')
    #abort_sweep_result.set("Status de l'envoi du fichier")

###############################################################################################

###############################################################################

# Fonction pour gérer l'action du bouton "select data folder"
def select_folder():
    Folder.clear()
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
def Download_Data(fileofinterest):
    global dir_folder
    if fileofinterest:
        selected_file_path= fileofinterest[0][1]
        AMPLIT=find(selected_file_path, 'AMPLIT', 1)
        OFFSET=find(selected_file_path, 'OFFSET', 1)
        FREQSTART=find(selected_file_path, 'FSWEEP', 2)
        FREQEND=find(selected_file_path, 'FSWEEP', 3)
        STEPS = find (selected_file_path, 'FSWEEP',1)
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
        path_to_logs = dir_folder[0]
        filename = f"GainPhase_AMP{AMPLIT}Vpk_OFS{OFFSET}V_{STEPS}pts_{FREQSTART}-{FREQEND}Hz_{datetime.datetime.now().strftime('%Y-%m-%d_%H.%M')}.csv"
        pathfile = f"{path_to_logs}/{filename}"
        with open(pathfile, "w", encoding="utf-8") as f: # remplacer test.csv par csvfilename qui est :csvfilename = str(f"GainPhase_AMP{AMPLIT}Vpk_OFS{OFFSET}V_{STEPS}pts_{FREQSTART}-{FREQEND}Hz_datetime.now().strftime('%Y-%m-%d_%H.%M').csv")
            f.write(results.replace("\r", ""))
            #f.write("Frequency,Magnitude_1,Magnitude_2,dB,Phase\n")
            #f.write(results)
    download_data_result.set("The data has been sent")

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
#########################################################################################################################################################################

# Créer la fenêtre principale
root = tk.Tk()
root.title("GP102 control board")

###############################################################################

###############################################################################

search_result = tk.StringVar()
search_port_button = tk.Button(root, text="Search Port Verification", command=update_search_result)
search_port_button.config(state="active")
search_port_button.grid(row=0, column=0, columnspan=2, sticky="ew")

# Create the text field to display the found port
search_port_entry = tk.Entry(root, textvariable=search_result, justify="center")
search_port_entry.config(fg="black")
search_port_entry.grid(row=0, column=2, sticky="ew")
###############################################################################

###############################################################################
# Créer le bouton "Upload source / config file"
# bug: append sur source integre un tableau dans un autre tableau, peu elegant.
source = []  # Initialize as an empty list
upload_button = tk.Button(root, text="Upload Config File", command=lambda: [source.append(upload_config()), update_entry(source, text_source)]) # append could be used as well
upload_button.config(state="active")
upload_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
text_source = tk.StringVar() # obliged to create a string variable compatible with tinker
upload_entry = tk.Entry(root, textvariable=text_source)
upload_entry.grid(row=1, column=2, sticky="ew")
file= source


###############################################################################

###############################################################################

# Créer le bouton "Send Config"

send_config_button = tk.Button(root, text="Send Config to TFA", command=lambda: send_config(file, port))
send_config_button.config(state="disabled")
send_config_button.grid(row=3, column=0, sticky="ew")


send_config_result = tk.StringVar()
send_config_entry = tk.Entry(root, textvariable=send_config_result)#, width=0, justify="center")
send_config_entry.grid(row=3, column=1,columnspan=2, sticky="ew")

###############################################################################

###############################################################################
# Créer le texte qui précède le bouton " View/Modify Config"
label = tk.Label(root, text="Display Config Settings :")
label.grid(row=2, column=0)

# Créer le bouton "generate Config"
view_config_button = tk.Button(root, text="View/Modify Config File", command=lambda: view_config(file))
view_config_button.config(state="disabled")
view_config_button.grid(row=2, column=1, sticky="ew")

###############################################################################

###############################################################################

# Créer le bouton "View signal(sinus)"
view_signal_button = tk.Button(root, text="View Sinusoidal Signal", command=lambda: view_signal(file))#,width=0)
view_signal_button.config(state="disabled")
view_signal_button.grid(row=2, column=2, sticky="ew")

###############################################################################

###############################################################################

# Créer le bouton "Start Sweep"
start_sweep_button = tk.Button(root, text="Start Sweep", command=lambda: Start_Sweep(port))
start_sweep_button.config(state="disabled")
start_sweep_button.grid(row=5, column=0,columnspan=1, sticky="ew")

# Créer le champ de texte à droite du bouton "start sweep" : c'est le status : sweeping / None / finish Sweeping
start_sweep_result = tk.StringVar()
start_sweep_entry = tk.Entry(root, textvariable=start_sweep_result)
start_sweep_entry.config(fg="red")
start_sweep_entry.grid(row=5, column=2, sticky="ew")

###############################################################################

###############################################################################

# Créer le bouton "Abort Sweep"
abort_sweep_button = tk.Button(root, text="Abort Sweep", command=lambda: Abort_Sweep(port))
abort_sweep_button.config(state="disabled")
abort_sweep_button.grid(row=5, column=1,columnspan=1, sticky="ew")

###############################################################################

###############################################################################

# Créer les boutons pour "generator control"

label = tk.Label(root, text="Generator Control :")
label.grid(row=4, column=0) # je créé du texte
generator_on_button = tk.Button(root, text="ON", command=turn_on)
generator_on_button.config(state="disabled")
generator_on_button.grid(row=4, column=1,columnspan=1, sticky="ew")
generator_off_button = tk.Button(root, text="OFF", command=turn_off)
generator_off_button.config(state="disabled")
generator_off_button.grid(row=4, column=2,columnspan=1, sticky="ew")

################################################################################

#################################################################################

# Créer le bouton "select data folder"
Folder=[]
data_folder_button = tk.Button(root, text="Select Data Folder", command=lambda: [Folder.extend(select_folder()), update_folder_entry(Folder, data_folder_result)])
data_folder_button.config(state="active")
data_folder_button.grid(row=6, column=0,columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Select data folder"
data_folder_result = tk.StringVar()
data_folder_entry = tk.Entry(root, textvariable=data_folder_result)
data_folder_entry.grid(row=6, column=2, sticky="ew")
dir_folder= Folder

###############################################################################

###############################################################################

# Créer le bouton "download data"
download_data_button = tk.Button(root, text="Download Data", command=lambda: Download_Data(file))
download_data_button.config(state="disabled")
download_data_button.grid(row=7, column=0,columnspan=2, sticky="ew")

# Créer le champ de texte à droite du bouton "Upload Config"
download_data_result = tk.StringVar()
download_data_entry = tk.Entry(root, textvariable=download_data_result)#, width=0, justify="center")
download_data_entry.grid(row=7, column=2, sticky="ew")

###############################################################################

###############################################################################
label = tk.Label(root, text="Time of Sweep (min;sec) :")
label.grid(row=8, column=0) # je créé du texte
# Créer le champ de texte à droite du bouton "Select data folder"
time_sweep_result = tk.StringVar()
time_sweep_entry = tk.Entry(root, textvariable=data_folder_result)
time_sweep_entry.grid(row=8, column=1, sticky="ew")

################################################################################

bouton_quit = tk.Button(root, text="Quit", command=button_quit, bg="#CC0000")
bouton_quit.grid(row=8, column=2)