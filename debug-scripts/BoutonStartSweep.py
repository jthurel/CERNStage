import tkinter as tk
import serial

# Définition de la fonction Start_Sweep
def Start_Sweep():
    with serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=2) as ser:
        ser.write(bytes("START", 'utf-8') + b'\r')

# Création de la fenêtre tkinter
root = tk.Tk()
root.title("Contrôle de la séquence")

# Création d'un bouton "Start"
start_button = tk.Button(root, text="Start", command=Start_Sweep)
start_button.pack(pady=20)

# Lancer la boucle principale de tkinter
root.mainloop()

###################################################################################################
# Fonction pour envoyer la commande "START" via la liaison série
def start_sweep(serial_port):
    ser = serial.Serial(serial_port, baudrate=19200, timeout=2)  # Ouvrez la liaison série avec le port spécifié
    ser.write(bytes("START", 'utf-8') + b'\r')
    ser.close()  # Fermez la liaison série après avoir envoyé la commande

# Créez le bouton "Start Sweep" et associez-le à la fonction start_sweep en passant le port en argument
start_button = tk.Button(root, text="Start Sweep", command=lambda: start_sweep("COM1"))  # Remplacez "COM1" par le nom du port que vous souhaitez utiliser
start_button.grid(row=2, column=0, columnspan=2, sticky="ew")