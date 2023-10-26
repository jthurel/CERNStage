import tkinter as tk
from tkinter import filedialog
import os
import time
import serial
import serial.tools.list_ports

# Déclarez ser comme une variable globale
ser = None

# Le reste de votre code

def search_port():
    global ser  # Utilisez la variable ser globale
    # port.device=""
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=19200, timeout=2)
            ser.write(bytes("*IDN?", 'utf-8') + b'\r')
            response = ser.readline().decode('ascii')
            ser.close()

            if "GP102" in response:
                return port.device
        except (OSError, serial.SerialException):
            continue

    return "Aucun port trouvé"



def Start_Sweep(port):
    global ser
    if ser is not None:
        with serial.Serial(port, baudrate=19200, timeout=2) as ser:
            ser.write(bytes("START", 'utf-8') + b'\r')
    else:
        print("Aucun port série n'est disponible.")


# Fonction pour gérer l'action du bouton "Abort sweep"
def Abort_Sweep(ser):
    ser.write(bytes("ABORT", 'utf-8') + b'\r')
    #abort_sweep_result.set("Status de l'envoi du fichier")
search_port()
Start_Sweep(ser)
#Abort_Sweep(ser)